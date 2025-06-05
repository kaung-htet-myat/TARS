import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
# from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
# from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchResults

from llm.tools import get_current_datetime, telegram_reminder_call


load_dotenv()


OLLAMA_URL = os.environ.get('OLLAMA_URL', '')
MODEL_NAME = os.environ.get('MODEL_NAME', 'llama3.1:8b-instruct-q4_1')
TEMPERATURE = os.environ.get('TEMPERATURE', 0.5)


def get_llm_agent():
    # llm = ChatOllama(
    #         model = MODEL_NAME,
    #         base_url = OLLAMA_URL,
    #         temperature = TEMPERATURE,
    #     )
    llm = ChatOpenAI(model='gpt-4o-mini')
    
    memory = MemorySaver()
    tools = [
        # DuckDuckGoSearchResults(max_results=2),
        get_current_datetime,
        telegram_reminder_call
    ]
    return create_react_agent(llm, tools, checkpointer=memory)
    