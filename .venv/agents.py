from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.agents import Agent
from dotenv import load_dotenv
from tools import web_search,scrape_url
load_dotenv()

llm = ChatMistralAI(model="mistral-small-2506")
