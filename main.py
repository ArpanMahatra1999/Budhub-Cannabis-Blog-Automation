# general libraries
import time

# functions
from website_functions import analyze_websites
from post_functions import generate_techniques, generate_blog, generate_headline
from document_functions import create_doc

if __name__ == "__main__":
    rss_feeds = ["https://www.the6ixcannabis.ca/blog/feed/",
                 "https://emilykylenutrition.com/feed/",
                 "https://cbdtesters.co/feed/"]

    # gather attributes and techniques
    attributes = analyze_websites(rss_feeds)
    print(attributes)
    time.sleep(30)
    techniques = generate_techniques(attributes)
    print(attributes)
    time.sleep(30)

    # generate blog and headline
    blog = generate_blog(attributes, techniques)
    print(blog)
    time.sleep(30)
    headline = generate_headline(blog, attributes)
    print(headline)

    # generate document
    create_doc(headline, blog)