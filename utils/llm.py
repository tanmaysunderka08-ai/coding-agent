import os
import time

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = None


class DailyLimitReached(Exception):
    pass


class LLMResult:
    def __init__(self):
        self.text = ""
        self.accepted = False 
        self.got_response = False
        self.calls = 0
        self.rejected = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.error = None


def get_client():
    global client
    if client is None:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise RuntimeError("GROQ_API_KEY not found in .env")
        client = Groq(api_key=key)
    return client


def is_daily_limit(message):
    m = message.lower()
    return "per day" in m or "(tpd)" in m or "(rpd)" in m


def call_llm(system, user, model, max_retries=5, temperature=0.2, validate=None):
    # validate(text) returns None if the reply is fine, else a short reason.
    # the reason is sent back to the model so the next try can fix it.
    res = LLMResult()
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    for attempt in range(1, max_retries + 1):
        res.calls += 1
        try:
            response = get_client().chat.completions.create(
                model=model, messages=messages, temperature=temperature,
            )
        except Exception as e:
            res.error = f"{type(e).__name__}: {e}"
            if is_daily_limit(str(e)):
                raise DailyLimitReached(res.error) from e
            print(f"[llm] call {attempt} failed: {res.error[:200]}")
            if attempt < max_retries:
                time.sleep(5 * 2 ** (attempt - 1))
            continue

        res.got_response = True
        if response.usage is not None:
            res.input_tokens += response.usage.prompt_tokens or 0
            res.output_tokens += response.usage.completion_tokens or 0

        res.text = (response.choices[0].message.content or "").strip()

        if not res.text:
            problem = "the reply was empty"
        elif validate is not None:
            problem = validate(res.text)
        else:
            problem = None

        if problem is None:
            res.accepted = True
            res.error = None
            return res

        res.rejected += 1
        res.error = f"unusable reply: {problem}"
        print(f"[llm] reply {attempt} rejected: {res.error[:200]}")
        messages = messages[:2] + [
            {"role": "assistant", "content": res.text},
            {"role": "user", "content": f"Your reply could not be used: {problem}\nReply again, following the required format exactly."},
        ]

    return res
