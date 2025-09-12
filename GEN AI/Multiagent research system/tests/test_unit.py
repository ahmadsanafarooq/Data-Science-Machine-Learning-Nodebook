import pytest
from src.agents.researcher import perform_research
from src.agents.summarizer import summarize_sources
from src.agents.writer import generate_report

def test_researcher_returns_list():
    topic = "Artificial Intelligence"
    results = perform_research(topic)
    assert isinstance(results, list)
    assert all(isinstance(r, str) for r in results)
    assert len(results) > 0, "Researcher should return at least one source"

def test_summarizer_returns_string():
    sources = ["AI is impacting finance.", "AI is transforming healthcare."]
    summary = summarize_sources(sources)
    assert isinstance(summary, str)
    assert len(summary.split()) > 10, "Summary too short"

def test_writer_returns_long_report():
    summary = "AI is used in healthcare for diagnostics and treatment."
    report = generate_report(summary)
    assert isinstance(report, str)
    assert len(report.split()) >= 100, "Writer output too short"
