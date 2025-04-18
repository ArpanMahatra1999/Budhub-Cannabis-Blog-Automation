# general libraries
import os
import time

# functions
from website_functions import analyze_websites
from post_functions import generate_techniques, generate_blog, generate_headline
from email_functions import send_email_with_attachment

if __name__ == "__main__":
    rss_feeds = ["https://www.the6ixcannabis.ca/blog/feed/",
                 "https://emilykylenutrition.com/feed/",
                 "https://cbdtesters.co/feed/"]

    # gather attributes and techniques
    attributes = analyze_websites(rss_feeds)
    print("------------------Attributes Created------------------")
    time.sleep(20)
    techniques = generate_techniques(attributes)
    print("------------------Techniques Created------------------")
    time.sleep(20)

    # generate blog and headline
    blog = generate_blog(attributes, techniques)
    print("------------------Blog Created------------------")
    time.sleep(20)
    headline = generate_headline(blog, attributes)
    print("------------------Headline Created------------------")

    # generate document
    send_email_with_attachment(
        sender="arpanmahatra1999ad@gmail.com",
        password=os.getenv("APP_PASSWORD"),
        receiver="arpanmahatra1999ad@gmail.com",
        subject=f"Today's blog on {headline}",
        body=f"""
            Hi Budhub,
            
            Here is your recent article on {headline}.
            Keywords: {attributes["keywords"]}
            
            Sincerely,
            Arpan
        """,
        headline=headline,
        description=blog
    )

