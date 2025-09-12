import gradio as gr
from workflows.research_workflow import run_research_workflow
from utils.exceptions import ValidationError
from utils.logger import get_logger

logger = get_logger(__name__)

# --- Guardrail: Input Validation ---
def validate_topic(topic: str) -> bool:
    if not topic or len(topic.strip()) < 5:
        raise ValidationError("❌ Topic too short or empty.")
    banned = ["hack", "exploit", "malware", "nsfw"]
    if any(word in topic.lower() for word in banned):
        raise ValidationError("❌ Topic contains banned content.")
    return True

# --- App Function ---
def start_research(topic: str):
    try:
        validate_topic(topic)  # guardrail before workflow
        report = run_research_workflow(topic)
        return report
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        return f"⚠️ Validation Error: {ve}"
    except Exception as e:
        logger.exception("Unexpected error during research workflow")
        return f"❌ Unexpected Error: {str(e)}"

# --- Gradio UI ---
def main():
    with gr.Blocks() as demo:
        gr.Markdown("# 🤖 Multi-Agent Research Assistant")
        topic_input = gr.Textbox(label="Enter Research Topic")
        output = gr.Textbox(label="Generated Report", lines=15)
        btn = gr.Button("Start Research")
        btn.click(start_research, inputs=topic_input, outputs=output)

    demo.launch()

if __name__ == "__main__":
    main()
