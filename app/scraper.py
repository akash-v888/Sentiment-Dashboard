# app/scraper.py

import certifi
import os
os.environ["SSL_CERT_FILE"] = certifi.where()
import snscrape.modules.twitter as sntwitter
import praw
from datetime import datetime
import pandas as pd


# Reddit API
reddit = praw.Reddit(
    client_id="l6V0G-WG0T1n7kHDhmmW9w",
    client_secret="uRc1GFf_qCg_lDoJtYconsAJB9xhJQ",
    password="akashviswanathan",
    user_agent="sentiment-dashboard-script by /u/sentiment-analyst-bo",
    username="sentiment-analyst-bo"
)


# Twitter Scraper
def scrape_twitter(keyword, max_results=20):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{keyword} since:2025-05-01").get_items()):
        if i >= max_results:
            break
        tweets.append({
            "timestamp": tweet.date.strftime("%Y-%m-%d %H:%M:%S"),
            "text": tweet.content,
            "source": "Twitter",
            "keyword": keyword
        })
    return tweets

# Reddit Scraper
def scrape_reddit(keyword, subreddit="all", max_results=20):
    posts = []
    for submission in reddit.subreddit(subreddit).hot(limit=max_results * 2):  # Overfetch to allow filtering
        if keyword.lower() in submission.title.lower() or keyword.lower() in (submission.selftext or "").lower():
            posts.append({
                "timestamp": datetime.fromtimestamp(submission.created_utc, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "text": submission.title + " " + (submission.selftext or ""),
                "source": "Reddit",
                "keyword": keyword
            })
        if len(posts) >= max_results:
            break
    return posts

# Combining scraped content
def get_combined_posts(keyword, max_results=20):
    reddit_posts = scrape_reddit(keyword, max_results=max_results)
    twitter_posts = scrape_twitter(keyword, max_results=max_results)
    all_posts = reddit_posts + twitter_posts
    return pd.DataFrame(all_posts)

# To CSV
if __name__ == "__main__":
    keyword = input("Enter a keyword to search: ")
    df = get_combined_posts(keyword)
    df.to_csv("data/sentiment_data.csv", index=False)
    print(f"Saved {len(df)} posts to data/sentiment_data.csv")
