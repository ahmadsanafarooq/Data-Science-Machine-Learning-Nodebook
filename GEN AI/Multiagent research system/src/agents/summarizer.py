from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from utils.logger import get_logger

logger = get_logger(__name__)

class Summarizer:
    def __init__(self, llm=None):
        self.llm = llm or ChatGroq(model="llama-3.1-8b-instant")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a summarizer. Condense the research into structured points."),
            ("human", "{research_text}")
        ])

    def run(self, research_text: str) -> str:
        logger.info("Summarizer started")
        try:
            chain = self.prompt | self.llm
            response = chain.invoke({"research_text": research_text})
            logger.info("Summarizer completed successfully")
            return response.content
        except Exception as e:
            logger.error(f"Summarizer failed: {e}")
            raise
