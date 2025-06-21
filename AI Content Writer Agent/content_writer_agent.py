# content_writer_agent.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain.prompts import PromptTemplate
from newspaper import Article
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

search = TavilySearchAPIWrapper()

tools = [
    Tool(
        name="Tavily Search",
        func=search.results,
        description="Search for articles on a topic"
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def extract_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def generate_blog_post(topic):
    print("🔍 Researching topic:", topic)
    results = search.results(topic)
    results = results[:3]  # Limit to 3

    summaries = []

    for r in results:
        try:
            url = r['url']
            print(f"📥 Reading: {url}")
            text = extract_article_text(url)
            prompt = PromptTemplate.from_template("Summarize the following article:\n{text}")
            summary_response = llm.invoke(prompt.format(text=text[:3000]))
            summaries.append(summary_response.content)
        except Exception as e:
            print(f"❌ Skipping URL due to error: {e}")
            continue

    if not summaries:
        return {
            "blog_post": "No summaries could be generated from the search results.",
            "seo": "N/A"
        }

    combined = "\n\n".join(summaries)

    blog_prompt = PromptTemplate.from_template(
        "Write a detailed blog post based on the following research summaries:\n\n{combined}"
    )
    blog_post = llm.invoke(blog_prompt.format(combined=combined)).content

    seo_prompt = PromptTemplate.from_template(
        "Create an SEO title, meta description, and 5 focus keywords for the topic: {topic}"
    )
    seo = llm.invoke(seo_prompt.format(topic=topic)).content

    return {
        "blog_post": blog_post,
        "seo": seo
    }
