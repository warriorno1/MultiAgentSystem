from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from tavily import TavilyClient
import requests
from bs4 import BeautifulSoup
import os
from rich import print

from langchain.tools import tool

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"));

@tool
def web_search(query: str)->str:
    """search the web for most relevent and latest news and returns titles,urls,snippets"""

    results = tavily.search(query);

    out = []

    for r in results['results']:
        out.append(
            f"title:{r['title']}\nUrl:{r['url']}\nSnippet:{r['content'][:300]}\n"
        )
    return "\n--------\n".join(out)
    

@tool
def scrape_url(url:str)->str:
    """scrape and extract text from url for better and deep reading"""

    try:
        response = requests.get(url,timeout=8,headers = {"user-agent":"mozilla/5.0"})
        soup = BeautifulSoup(response.text,"html.parser")
        for tag in soup(['script','style','nav','footer']):
            tag.decompose()
        return soup.get_text(separator=" ",strip=True)[:3000]
    except Exception as e:
        return f"couldn't find scrap url : {str(e)} "


print(scrape_url.invoke("https://edition.cnn.com/2026/08/26/weather/floods-nepal-cause-vis"))





#print(web_search.invoke("give me the news about nepal flood"))


