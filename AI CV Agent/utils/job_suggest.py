from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

def suggest_jobs(cv_text, preferences=""):
    prompt = f"""
    Based on the following CV and the user's job preferences: {preferences}, recommend 3 relevant job titles.
    Provide brief explanations for each match.

    CV:
    {cv_text}
    """
    return llm.invoke(prompt).content
