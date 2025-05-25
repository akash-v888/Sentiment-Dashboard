# app/twitter_scraper.py

import subprocess
import json
import pandas as pd

def scrape_twitter(keyword, max_results=20):
    tweets = []
    try:
        cmd = [
            "snscrape",
            "--jsonl",
            "--max-results",
            str(max_results),
            f"twitter-search:{keyword} since:2025-05-01"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            tweet = json.loads(line)
            tweets.append({
                "timestamp": tweet['date'][:19].replace("T", " "),
                "text": tweet['content'],
                "source": "Twitter",
                "keyword": keyword
            })
    except subprocess.CalledProcessError as e:
        print("Twitter scraping failed:", e)
    return pd.DataFrame(tweets)

if __name__ == "__main__":
    keyword = input("Enter keyword for Twitter: ")
    df = scrape_twitter(keyword)
    df.to_csv("data/twitter_data.csv", index=False)
    print(f"Saved {len(df)} Twitter posts to data/twitter_data.csv")
