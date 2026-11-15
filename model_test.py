# quick speed test: groq api vs a local ollama model, same prompt

import os
import time

import ollama
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def test_groq(prompt, model="openai/gpt-oss-120b"):
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content, time.time() - start


def test_ollama(prompt, model="llama3.1"):
    start = time.time()
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"], time.time() - start


if __name__ == "__main__":
    prompt = "Write a simple Python function to calculate the Fibonacci sequence. Keep it under 5 lines."

    _, groq_time = test_groq(prompt)
    print(f"groq: {groq_time:.2f} s")

    _, ollama_time = test_ollama(prompt)
    print(f"ollama: {ollama_time:.2f} s")

    print(f"groq was {ollama_time / groq_time:.1f}x faster")
