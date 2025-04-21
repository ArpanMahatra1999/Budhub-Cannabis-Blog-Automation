# general libraries
import os
import json
import time

from dotenv import load_dotenv

# parsing libraries
import feedparser

# generative ai libraries
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# load environment variables
load_dotenv()


def generate_attributes(blog_lists):
    """Generate one topic, multiple urls, summaries and keywords from blog lists"""
    prompt_template = """
        We are the Budhub Cannabis in Etobicoke, ON.
        By studying blog lists below, generate the most trending topic (not related to blog writing company) from different websites and 
        list 2-3 urls from links related to trending topic and their summaries.
        
        Blog lists: {blog_lists}
        
        Respond in JSON format like this:
        {{
            "topic": "Catchy topic of maximum 10 words."
            "related_urls": "List of links from blog lists related to topic generated above."
            "related_summaries": "List of summaries related to related urls."
            "keywords": "List of top keywords from related summaries."
        }}
        
        Additional Details:
        - Topic should be relevant to write blog into BUDHUB CANNABIS website.
        - Don't use all related urls from same website.
        - Summaries must be rewritten like they don't target blogging company.
        - Keywords must not be company oriented.
    """
    prompt = PromptTemplate(
        input_variables=["topic"],
        template=prompt_template
    )
    llm = ChatOpenAI(
        temperature=1.0,
        max_tokens=1024,
        model_name=os.getenv("OPENAI_MODEL_NAME"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    chain = prompt | llm
    attributes = chain.invoke({"blog_lists": blog_lists}).content
    return json.loads(attributes[attributes.find('{'): attributes.rfind('}')+1])


def analyze_websites(rss_feeds):
    """
    Gather topic, summaries, urls and keywords from rss_feeds
    """
    blog_lists = list()
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:2]:
            blog_lists.append({'title': entry.title,
                               'summary': entry.description,
                               'link': entry.link})
            print("Blog Appended")

    return generate_attributes(blog_lists)