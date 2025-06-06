import praw
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import pandas as pd

load_dotenv()

# Reddit API setup
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def scrape_reddit(keyword, subreddits=None, posts_per_sub=30):
    if subreddits is None:
        subreddits = [
            "technology", "ArtificialInteligence", "computerscience",
            "datascience", "news", "chatgpt", "all"
        ]

    posts = []

    for sub in subreddits:
        try:
            print(f"Fetching from r/{sub}")
            for submission in reddit.subreddit(sub).hot(limit=posts_per_sub):
                full_text = submission.title + " " + (submission.selftext or "")
                posts.append({
                    "timestamp": datetime.fromtimestamp(submission.created_utc, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                    "subreddit": sub,
                    "text": full_text,
                    "source": "Reddit",
                    "keyword": keyword
                })
        except Exception as e:
            print(f"Skipping r/{sub}: {e}")

    return pd.DataFrame(posts)

if __name__ == "__main__":
    keyword = input("Enter keyword for Reddit: ").strip()
    df = scrape_reddit(keyword)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/reddit_data.csv", index=False)
    print(f"Saved {len(df)} Reddit posts to data/reddit_data.csv")
