import pytest
from src.agents.researcher import perform_research
from src.agents.summarizer import summarize_sources
from src.agents.writer import generate_report

def test_research_to_summary():
    research_output = perform_research("Quantum Computing")
    summary = summarize_sources(research_output)
    assert "quantum" in summary.lower()

def test_summary_to_writer():
    summary_text = "Quantum computing has applications in cryptography and optimization."
    report = generate_report(summary_text)
    assert len(report.split()) >= 200, "Report not long enough"
