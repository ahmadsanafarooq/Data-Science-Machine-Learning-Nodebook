from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

def suggest_improvements(cv_text):
    prompt = f"""
    You are a professional resume coach. Analyze this CV and provide:
    - At least 3 actionable suggestions
    - Highlight grammar or formatting issues
    - Recommend keyword improvements for better ATS performance

    CV:
    {cv_text}
    """
    return llm.invoke(prompt).content
