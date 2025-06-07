from langchain_openai import ChatOpenAI

# from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
# from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchResults

from llm.tools import get_current_datetime, telegram_reminder_call


def get_llm_agent(openai_api_key: str):
    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key)

    memory = MemorySaver()
    tools = [
        # DuckDuckGoSearchResults(max_results=2),
        get_current_datetime,
        telegram_reminder_call,
    ]
    return create_react_agent(llm, tools, checkpointer=memory)
