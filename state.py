from pydantic import BaseModel, Field


class AgentState(BaseModel):
    task_dir: str
    task_id: str = ""
    model_name: str = "openai/gpt-oss-120b"
    max_loops: int = 3
    max_llm_retries: int = 5

    # code[0] = original code, code[i] = code after fix i
    code: list[str] = Field(default_factory=list)
    # compiler_msg[0] = pytest on the buggy code, compiler_msg[i] = after fix i
    compiler_msg: list[str] = Field(default_factory=list)
    # plans as text (for prompts) and as data (for the csv)
    strategy: list[str] = Field(default_factory=list)
    plans: list[dict] = Field(default_factory=list)

    sandbox_exit_code: int = -1
    main_loop_count: int = Field(default=0, ge=0)
    llm_retry_count: int = Field(default=0, ge=0)   # every api call, retries too
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
