from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from utils.logger import get_logger

logger = get_logger(__name__)

class Writer:
    def __init__(self, llm=None):
        self.llm = llm or ChatGroq(model="llama-3.1-70b-versatile")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a writer. Convert summaries into a polished report."),
            ("human", "{summary_text}")
        ])

    def run(self, summary_text: str) -> str:
        logger.info("Writer started")
        try:
            chain = self.prompt | self.llm
            response = chain.invoke({"summary_text": summary_text})
            logger.info("Writer completed successfully")
            return response.content
        except Exception as e:
            logger.error(f"Writer failed: {e}")
            raise
