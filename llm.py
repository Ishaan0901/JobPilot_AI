from langchain_groq import ChatGroq
from tools.job_search import job_search
from tools.search_tool import search_tool
from tools.RAG_Tool import RAG_tool
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b"
)
tools=[search_tool,RAG_tool,job_search]

llm_with_tools=llm.bind_tools(tools)