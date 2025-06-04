from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from agent.prompts import EXPLAIN_PROMPT, DEBUG_PROMPT
from agent.tools import explain_code, generate_code, debug_code

llm = ChatOpenAI(temperature=0)

tools = [
    Tool(name="Explain Code", func=explain_code, description="Explains a piece of code"),
    Tool(name="Generate Code", func=generate_code, description="Generates code from a prompt"),
    Tool(name="Debug Code", func=debug_code, description="Helps debug Python code with an error")
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

def run_agent(user_input):
    return agent.run(user_input)
