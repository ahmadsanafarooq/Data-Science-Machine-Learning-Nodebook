from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from utils.logger import get_logger

logger = get_logger(__name__)

class Researcher:
    def __init__(self, llm=None):
        self.llm = llm or ChatGroq(model="llama-3.1-70b-versatile")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a research agent. Search, collect, and summarize information."),
            ("human", "{topic}")
        ])

    def run(self, topic: str) -> str:
        logger.info(f"Researcher started with topic: {topic}")
        try:
            chain = self.prompt | self.llm
            response = chain.invoke({"topic": topic})
            logger.info("Researcher completed successfully")
            return response.content
        except Exception as e:
            logger.error(f"Researcher failed: {e}")
            raise
