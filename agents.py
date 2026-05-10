from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search , scrape_url
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(model_name: str = "llama-3.1-8b-instant"):
    try:
        return ChatGroq(model_name=model_name, temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"))
    except Exception:
        return ChatGroq(model_name="llama-3.1-8b-instant", temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"))

##first Agent##

def build_search_agent(model_name: str = "llama-3.1-8b-instant"):
    return create_react_agent(
        model=get_llm(model_name),
        tools=[web_search],
        prompt="You are a research assistant. Your ONLY available tool is web_search. Do NOT use or invent any other tools. Find the best information for the user's query."
    )

##second Agent##

def build_reader_agent(model_name: str = "llama-3.1-8b-instant"):
    return create_react_agent(
        model=get_llm(model_name),
        tools=[scrape_url],
        prompt="You are a reading assistant. Your ONLY available tool is scrape_url. Do NOT use or invent any other tools (like brave_search). If you cannot find a valid URL to scrape, just output a summary based on the text provided."
    )


##writer chain##

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

def get_writer_chain(model_name: str = "llama-3.1-8b-instant"):
    return writer_prompt | get_llm(model_name) | StrOutputParser()

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

def get_critic_chain(model_name: str = "llama-3.1-8b-instant"):
    return critic_prompt | get_llm(model_name) | StrOutputParser()