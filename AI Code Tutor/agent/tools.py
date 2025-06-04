from langchain.llms import OpenAI
from agent.prompts import EXPLAIN_PROMPT, DEBUG_PROMPT

llm = OpenAI(temperature=0)

def explain_code(code: str) -> str:
    prompt = EXPLAIN_PROMPT.format(code=code)
    return llm(prompt)

def generate_code(prompt: str) -> str:
    return llm(f"Write Python code for the following: {prompt}")

def debug_code(code: str) -> str:
    prompt = DEBUG_PROMPT.format(code=code)
    return llm(prompt)
