from flask import Flask, render_template, request
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Optionally, you can fetch your API key here if needed
# api_key = os.getenv("GOOGLE_API_KEY")

app = Flask(__name__)

# Initialize LLM with your desired model and parameters
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)


def explain_code(code: str) -> str:
    """Send a prompt to explain Python code."""
    return llm.invoke(f"Explain this Python code:\n```python\n{code}\n```")


def generate_code(prompt: str) -> str:
    """Send a prompt to generate minimal Python syntax with example, no explanation."""
    return llm.invoke(f"Provide only the basic syntax and a minimal example for {prompt} in python. No explanations.")


def debug_code(code: str) -> str:
    """Send a prompt to debug given Python code."""
    return llm.invoke(f"Debug this Python code:\n```python\n{code}\n```")


def clean_code_response(message) -> str:
    """
    Extract clean text from LLM response.
    Handles AIMessage object or plain string.
    Removes triple backticks and fixes escaped newlines.
    """
    text = message.content if hasattr(message, "content") else str(message)
    
    # Remove triple backticks and optional language tag for code blocks
    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    
    # Remove inline backticks `code`
    text = re.sub(r"`([^`]*)`", r"\1", text)
    
    # Remove bold **text** or __text__
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    
    # Remove italic *text* or _text_
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)
    
    # Replace literal escaped newlines (\n) with actual newlines
    text = text.replace("\\n", "\n")
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    user_input = ""
    selected_action = "Explain Code"

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        selected_action = request.form.get("action", "Explain Code")

        if not user_input:
            response_text = "⚠️ Please enter some code or prompt."
        else:
            if selected_action == "Explain Code":
                raw_response = explain_code(user_input)
                response_text = clean_code_response(raw_response)
            elif selected_action == "Generate Code":
                raw_response = generate_code(user_input)
                response_text = clean_code_response(raw_response)
            elif selected_action == "Debug Code":
                raw_response = debug_code(user_input)
                response_text = clean_code_response(raw_response)

    return render_template(
        "index.html",
        response=response_text,
        user_input=user_input,
        selected_action=selected_action,
    )


if __name__ == "__main__":
    # Run on all network interfaces for testing, disable debug in production
    app.run(debug=True, host="0.0.0.0", port=5000)
