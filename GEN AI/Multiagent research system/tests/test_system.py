from main import run_research_workflow

def test_full_workflow():
    topic = "AI in Healthcare"
    report = run_research_workflow(topic)
    assert isinstance(report, str)
    assert len(report.split()) >= 500, "Report should be at least 500 words"
    assert "healthcare" in report.lower(), "Report should mention the topic"
