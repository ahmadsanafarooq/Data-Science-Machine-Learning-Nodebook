import os
import gradio as gr
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun


load_dotenv()


try:
    google_api_key = os.environ["GOOGLE_API_KEY"]
except KeyError:
    raise ValueError("GOOGLE_API_KEY not found. Please set it as an environment variable.")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=google_api_key
)

# Define Custom Tools using LangChain's @tool decorator ---
# These tools are fully compatible with the LangChain framework.
search_tool = DuckDuckGoSearchRun()

# A custom tool for scraping a website's content
@tool
def scrape_website(url: str) -> str:
    """
    Scrapes the text content from a given URL, returning a string.
    This tool fetches the HTML and extracts visible text content.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        text_content = soup.get_text(separator=' ', strip=True)
        return text_content[:4000]
    except requests.exceptions.RequestException as e:
        return f"Error scraping website: {e}"

#  Define Prompts for Each Agent Role 
researcher_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a Senior Research Analyst. Your goal is to uncover groundbreaking technologies and trends. You have access to tools for searching and scraping websites. Always use your tools to find the most relevant and up-to-date information."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

summarizer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a Professional Summarizer. Your task is to take raw research data and distill it into a clear, concise summary. Your primary goal is to extract key findings, major players, and potential future impacts from the provided text."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

writer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a Senior Technology Report Writer. You must compose a comprehensive, well-structured report. Use the provided summary as the basis for your writing. The final output MUST be the full text of the report, not a summary of what you did."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Create AgentExecutor Instances for Each Agent 
researcher_tools = [search_tool, scrape_website]
researcher_agent = create_tool_calling_agent(llm, researcher_tools, researcher_prompt)
researcher_executor = AgentExecutor(agent=researcher_agent, tools=researcher_tools, verbose=True)

summarizer_tools = [search_tool]
summarizer_agent = create_tool_calling_agent(llm, summarizer_tools, summarizer_prompt)
summarizer_executor = AgentExecutor(agent=summarizer_agent, tools=summarizer_tools, verbose=True)


writer_tools = []
writer_agent = create_tool_calling_agent(llm, writer_tools, writer_prompt)
writer_executor = AgentExecutor(agent=writer_agent, tools=writer_tools, verbose=True)


def run_research_workflow(topic):

    print("\n--- Starting Researcher Agent ---")
    research_input = f"Find the top 3-5 trends for the topic: {topic}. For each trend, find relevant articles and summarize why they are important."
    research_output = researcher_executor.invoke({"input": research_input, "chat_history": []})['output']
    print(f"\nResearcher Output:\n{research_output}")

 
    print("\n--- Starting Summarizer Agent ---")
    summarizer_input = f"Summarize the following research findings into a 2-3 paragraph summary:\n\n{research_output}"
    summary_output = summarizer_executor.invoke({"input": summarizer_input, "chat_history": []})['output']
    print(f"\nSummarizer Output:\n{summary_output}")

    print("\n--- Starting Writer Agent ---")
    writer_input = f"Using the following summary, compose a comprehensive report of at least 500 words, with an introduction, body, and conclusion.\n\nSummary:\n{summary_output}"
    report_output = writer_executor.invoke({"input": writer_input, "chat_history": []})['output']
  
    file_path = 'research_report.md'
    try:
        with open(file_path, 'w') as f:
            f.write(report_output)
        print(f"\nFinal report saved to '{file_path}'.")
    except Exception as e:
        print(f"Error writing report to file: {e}")
        
    return report_output


def run_app(topic):
    if not topic:
        return "Please enter a research topic."
    
    try:
        report = run_research_workflow(topic)
        return report
    except Exception as e:
        return f"An error occurred during the workflow: {str(e)}"


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Multi-Agent Research Assistant (LangChain Only)")
    gr.Markdown("Enter a topic below and the AI agents will collaborate to create a research report for you.")
    
    with gr.Row():
        topic_input = gr.Textbox(label="Research Topic", placeholder="e.g., The Future of AI in Healthcare")
    
    submit_button = gr.Button("Start Research")
    
    gr.Markdown("## Research Report")
    output_text = gr.Markdown(label="Generated Report")

    submit_button.click(
        fn=run_app,
        inputs=[topic_input],
        outputs=[output_text]
    )

if __name__ == "__main__":
    demo.launch()