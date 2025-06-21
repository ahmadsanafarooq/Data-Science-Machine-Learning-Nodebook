from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from dotenv import load_dotenv

# Load API key
load_dotenv()
search = TavilySearchAPIWrapper()
print(dir(search))
