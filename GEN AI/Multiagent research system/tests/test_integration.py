from main import researcher_executor, summarizer_executor, writer_executor

def test_research_to_summary():
    research_output = researcher_executor.invoke({"input": "Trends in Quantum Computing", "chat_history": []})['output']
    summary_output = summarizer_executor.invoke({"input": f"Summarize: {research_output}", "chat_history": []})['output']
    assert "quantum" in summary_output.lower(), "Summary does not mention topic"

def test_summary_to_writer():
    summary_text = "Quantum computing has applications in cryptography and optimization."
    report_output = writer_executor.invoke({"input": f"Write report: {summary_text}", "chat_history": []})['output']
    assert len(report_output.split()) >= 200, "Report not long enough"
