import pytest
from main import researcher_executor, summarizer_executor, writer_executor

def test_researcher_agent():
    output = researcher_executor.invoke({"input": "Find AI trends", "chat_history": []})['output']
    assert isinstance(output, str)
    assert len(output) > 50, "Researcher output too short"

def test_summarizer_agent():
    fake_research = "AI is advancing in healthcare, robotics, and education."
    output = summarizer_executor.invoke({"input": f"Summarize: {fake_research}", "chat_history": []})['output']
    assert "AI" in output, "Summarizer did not mention AI"
    assert len(output.split()) > 20, "Summary too short"

def test_writer_agent():
    fake_summary = "AI is advancing in healthcare and robotics."
    output = writer_executor.invoke({"input": f"Write report: {fake_summary}", "chat_history": []})['output']
    assert len(output.split()) >= 100, "Writer output too short"
