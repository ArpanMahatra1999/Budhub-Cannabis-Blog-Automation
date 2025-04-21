# general libraries
import os
from dotenv import load_dotenv
import json

# generative ai libraries
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


# load environment variables
load_dotenv()


def generate_techniques(attributes):
    """Find novelty and 5 answers for writing blog"""
    prompt_template = """
        You are the Budhub Cannabis company blogger in Ontario preparing for writing blog.
        
        Use topic, summaries and keywords for tasks below:
        topic: {topic}
        summaries: {summaries}
        keywords: {keywords}
        
        Choose only one among 5 novelty categories below to write a blog:
        - Counter-intuitive (Oh, I never realized the world worked that way.)
        - Counter-narrative (Wow, that’s not how I was told the world worked!)
        - Shock and awe (That’s crazy. I would have never believed it.)
        - Elegant articulations (Beautiful. I couldn’t have said it better myself.)
        - Make someone feel seen (Yes! That’s exactly how I feel!)
        
        Generate relevant answers to 5 questions below too:
        - Do you have personal experience with this topic "{topic}"?
        - Can you tell about latest research and findings relevant to this topic "{topic}"?
        - Can you invite readers for opinions and ideas in this topic "{topic}"?
        - Can you provide data or back opinion with science in this topic "{topic}"?
        - Do you have opinion opposite to famous opinion in this topic "{topic}"?
        
        You just need to select novelty category and answer 5 questions.
        
        Respond in JSON format like below:
        {{
            "novelty": "Write only one novelty category in String format."
            "Do you have personal experience with this topic?": "Answer of this question as string.",
            "Can you tell about latest research and findings relevant to this topic?": "Answer of this question as string.",
            "Can you invite readers for opinions and ideas in this topic?": "Answer of this question as string.",
            "Can you provide data or back opinion with science in this topic?": "Answer of this question as string.",
            "Do you have opinion opposite to famous opinion in this topic?": "Answer of this question as string."
        }}
    """
    prompt = PromptTemplate(
        input_variables=["topic", "summaries", "keywords"],
        template=prompt_template
    )
    llm = ChatOpenAI(
        temperature=1.0,
        max_tokens=1024,
        model_name=os.getenv("OPENAI_MODEL_NAME"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    chain = prompt | llm
    novelty_and_answers = chain.invoke({"topic": attributes["topic"], "summaries": attributes["related_summaries"], "keywords": attributes["keywords"]}).content
    return json.loads(novelty_and_answers[novelty_and_answers.find("{"): novelty_and_answers.rfind("}")+1])


def generate_blog(attributes, techniques):
    """Generate blog of description only"""
    prompt_template = """
        You are the blog writer for Budhub Cannabis. Write a blog with only description (not including title).
        
        Use following information:
        {techniques}
        Topic: {topic}
        Summaries: {summaries}
        Keywords: {keywords}
        References: {references}
        
        Additional details:
        - Target the topic.
        - Give attractive starting to the blog like: TELLING QUOTE, ASKING QUESTION, PRESENTING EXAMPLE.
        - Use novelty technique to write the blog.
        - Try to include the information from those summaries.
        - Use relevant examples and true numbers than support claim.
        - Give headings for dividing blog properly.
        - Use paragraphs and bullets while writing.
        - Add references in the very end.
        - Try to use relevant answers (not questions) on the blog.
        - Use keywords to make blog friendlier to readers.
        - Don't use same keywords illogically multiple times.
        - Don't include major title.
        
        Respond the complete blog in String format.
        Your writing should be UNIQUE that doesn't look like copied from other summaries.
    """
    prompt = PromptTemplate(
        input_variables=["techniques", "topic", "summaries", "keywords", "references"],
        template=prompt_template
    )
    llm = ChatOpenAI(
        temperature=1.0,
        max_tokens=1024,
        model_name=os.getenv("OPENAI_MODEL_NAME"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    chain = prompt | llm
    return chain.invoke({
        "techniques": techniques,
        "topic": attributes["topic"],
        "summaries": attributes["related_summaries"],
        "keywords": attributes["keywords"],
        "references": attributes["related_urls"]
    }).content


def generate_headline(blog, attributes):
    """Generate headline relevant to blog"""
    prompt_template = """
        Generate headline for blog below using keywords and headline writing tips.
        
        Blog: {blog}
        Keywords: {keywords}
        
        Headline Writing Tips (Required):
        - Starting your headline with a number helps headline standing out.
        - Define what the article is about. eg: How to Compose Your Own Song: Songwriting 101
        - Explain your readers why your article is worth reading.
        - Provide a chance to read about how we are being manipulated, deceived, or given the runaround.
        - Think of creative ways to present a “how to” educational article without using "how to". eg: 6 Strategies for Deterring Burglars
        - Readers Should be EXCITED to Read Your Article.
        
        Headline Writing Tips (Optional)
        - Best blog post headlines aren’t afraid to sell themselves. So, don't be afraid.
        - Create an Eye-Catching, Unique Title.
        - Think About Your Audience and What Matters to Them.
        - Remember the 5Ws: Who, What, When, Where, Why.
        - Address Readers in 2nd Person.
        - Break Conventions. eg: Why the iPhone 5 is a Piece of Crap.
        - Brainstorm Lots of Different Headlines.
        - Use Strong Adjectives and Verbs.
        - Ask Questions. eg: Think You Know SEO? Quiz Yourself and Find Out!
        - Try to use keywords as provided.
        - Don’t Forget to A/B Test. Take 2-3 deadlines that potentially perform well and compare them.
        
        Respond the complete headline in String Format with maximum 70 characters including spaces.
    """
    prompt = PromptTemplate(
        input_variables=["blog", "keywords"],
        template=prompt_template
    )
    llm = ChatOpenAI(
        temperature=1.0,
        max_tokens=1024,
        model_name=os.getenv("OPENAI_MODEL_NAME"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    chain = prompt | llm
    return chain.invoke({"blog": blog, "keywords": attributes["keywords"]}).content


def rewrite_blog(headline, blog, keywords):
    """Rewrite blog properly based on headline and keywords"""
    prompt_template = """
        Rewrite blog relevant to headline and keywords.

        Blog: {blog}
        Keywords: {keywords}

        Additional details:
        - Target the headline.
        - Give attractive starting to the blog like: TELLING QUOTE, ASKING QUESTION, PRESENTING EXAMPLE.
        - Use relevant examples and true numbers than support claim.
        - Use paragraphs and bullets while writing.
        - Add references in the very end.
        - Use keywords to make blog friendlier to readers.
        - Don't use same keywords illogically multiple times.
        - Don't include headline here.
        
        Respond the completely rewritten blog in String format.
        Humanize text and Proofread the blog completely in the end.
    """
    prompt = PromptTemplate(
        input_variables=["headline", "blog", "keywords"],
        template=prompt_template
    )
    llm = ChatOpenAI(
        temperature=1.0,
        max_tokens=1024,
        model_name=os.getenv("OPENAI_MODEL_NAME"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    chain = prompt | llm
    return chain.invoke({"headline": headline, "blog": blog, "keywords": keywords}).content