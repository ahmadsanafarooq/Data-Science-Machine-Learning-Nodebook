from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

def get_rts_score(cv_text):
    prompt = f"""
    You are a CV evaluator. Rate this CV from 0-100 on the following:
    - Formatting
    - Grammar
    - Relevance to job roles
    - Use of keywords
    - Logical structure

    Provide an RTS score and explanation for each category.

    CV:
    {cv_text}
    """
    return llm.invoke(prompt).content
