from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
from langchain.agents import create_agent
from tools import web_search,scrape_url
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

llm = ChatMistralAI(model="mistral-small-2506")

def build_search_agent():
    return create_agent(
        model = llm,
        tools = [web_search]
    )

def build_reader_agent():
    return create_agent(
        model=llm,
        tools = [scrape_url]
    )

writer_prompt = ChatPromptTemplate.from_messages([
    ("system","you are an expert research writer. write clean,stretured and insightful reports."),
    ("human","""write a detailed research report on the topic below

Topic: {topic}

Research Gathered:
{research}

Strecture the report as:
- Introduction
-Key Findings (minimum 3 well explained points)
-conlusion 
-Sources (list all urls found in the research)

Be detailed, fatual amd professional"""
    ),
]

)

writer_chain = writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    ("system","you are a sharp and onstrutive researh riti. Be honest and speifi"),
    ("human","""review the researh report below and evaluate it stritly.
    

    Report:
    {report}

    Respond in this exact form:

    score: x/10

    Strenghts:
    - xxx
    -xxx

    Areas to improve:
    -xxxx
    -xxxx

    one line verdit:
    ....
    """)
])

critic_chain = critic_prompt | llm | StrOutputParser()

