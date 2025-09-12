from agents.researcher import ResearcherAgent
from agents.summarizer import SummarizerAgent
from agents.writer import WriterAgent
from utils.exceptions import ValidationError
from utils.logger import get_logger

logger = get_logger(__name__)

# --- Guardrail: Output Validation ---
def validate_output(output: str, step: str) -> str:
    if not output or len(output.strip()) < 20:
        raise ValidationError(f"❌ {step} produced invalid/empty output.")
    return output

# --- Orchestrated Workflow ---
def run_research_workflow(topic: str) -> str:
    logger.info(f"🚀 Starting workflow for topic: {topic}")

    researcher = ResearcherAgent()
    summarizer = SummarizerAgent()
    writer = WriterAgent()

    # Step 1: Research
    research = researcher.run(topic)
    research = validate_output(research, "Researcher")
    logger.info("✅ Researcher step completed.")

    # Step 2: Summarization
    summary = summarizer.run(research)
    summary = validate_output(summary, "Summarizer")
    logger.info("✅ Summarizer step completed.")

    # Step 3: Writing
    report = writer.run(summary)
    report = validate_output(report, "Writer")
    logger.info("✅ Writer step completed.")

    logger.info("🎉 Workflow completed successfully.")
    return report