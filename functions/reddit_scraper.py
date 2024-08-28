import pandas as pd
import praw
import re
import html
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize PRAW with your credentials
my_client_id = os.getenv('CLIENT_ID')
my_client_secret = os.getenv('CLIENT_SECRET')
my_user_agent = os.getenv('USER_AGENT')

reddit = praw.Reddit(
    client_id=my_client_id,
    client_secret=my_client_secret,
    user_agent=my_user_agent,
)

def clean_text(text):
    # Unescape HTML entities
    text = html.unescape(text)
    
    # Remove Markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)  # Remove italic
    text = re.sub(r'__(.*?)__', r'\1', text)  # Remove underline
    text = re.sub(r'~~(.*?)~~', r'\1', text)  # Remove strikethrough
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Replace newlines with spaces
    text = text.replace('\n', ' ')
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

#pass in subreddit name and number of desired stories
def scrape_subreddit(subreddit_name, num_of_stories):
    # Choose a subreddit and scrape submissions
    subreddit = reddit.subreddit(subreddit_name)

    scraped_stories = []

    for submission in subreddit.hot(limit=num_of_stories):
        cleaned_text = clean_text(submission.selftext)
        scraped_stories.append({
            'ID': submission.id,
            "Title": clean_text(submission.title),
            "Score": submission.score,
            "Comments": submission.num_comments,
            "Text": cleaned_text,
            "URL": submission.url
        })

    df = pd.DataFrame(scraped_stories)

    # Use escapechar when writing to CSV to handle any remaining double quotes
    df.to_csv('reddit_scraped_data.csv', index=False, escapechar='\\')

