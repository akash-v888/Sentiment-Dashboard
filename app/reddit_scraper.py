import praw
from datetime import datetime, timezone
import pandas as pd

# Reddit API
reddit = praw.Reddit(
    client_id="l6V0G-WG0T1n7kHDhmmW9w",
    client_secret="uRc1GFf_qCg_lDoJtYconsAJB9xhJQ",
    password="akashviswanathan",
    user_agent="sentiment-dashboard-script by /u/sentiment-analyst-bo",
    username="sentiment-analyst-bo"
)

def scrape_reddit(keyword, subreddits=["technology", "ArtificialInteligence", "computerscience", "datascience", "news"], posts_per_sub=30):
    posts = []
    for sub in subreddits:
        try:
            print(f"Fetching from r/{sub}")
            for submission in reddit.subreddit(sub).hot(limit=posts_per_sub):
                text = (submission.title + " " + (submission.selftext or "")).lower()
                if keyword.lower() in text:
                    posts.append({
                        "timestamp": datetime.fromtimestamp(submission.created_utc, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                        "subreddit": sub,
                        "text": submission.title + " " + (submission.selftext or ""),
                        "source": "Reddit",
                        "keyword": keyword
                    })
        except Exception as e:
            print(f"Skipping r/{sub}: {e}")
    return pd.DataFrame(posts)

if __name__ == "__main__":
    keyword = input("Enter keyword for Reddit: ")
    df = scrape_reddit(keyword)
    df.to_csv("data/reddit_data.csv", index=False)
    print(f"Saved {len(df)} Reddit posts to data/reddit_data.csv")
