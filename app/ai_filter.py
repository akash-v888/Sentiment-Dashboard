import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_SECRET"))

def ai_is_useful(text: str, keyword: str) -> bool:
    """Uses OpenAI to determine if text is relevant to the given keyword."""
    try:
        prompt = f"""
You are evaluating whether a social media post is relevant for analyzing public opinion about the keyword: "{keyword}".

If the post clearly discusses the keyword directly or indirectly (through commentary, opinions, news, or questions), respond with YES.
If it is unrelated, off-topic, or only mentions the keyword in passing, respond with NO.

Respond ONLY with YES or NO.

Post:
{text}
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=[
                {"role": "system", "content": "You evaluate whether posts are relevant to a topic for sentiment analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        reply = response.choices[0].message.content.strip().upper()
        return reply.strip().upper().startswith("YES")
    except Exception as e:
        print(f"Error from OpenAI API: {e}")
        return False

def filter_file(path: str, keyword: str) -> pd.DataFrame:
    """Filter a CSV of posts using OpenAI GPT relevance check."""
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return pd.DataFrame()
    df = pd.read_csv(path)
    if "text" not in df.columns:
        print(f"'text' column missing in {path}")
        return pd.DataFrame()
    
    filtered_rows = []
    for _, row in df.iterrows():
        text = row.get("text", "")
        if not text:
            continue
        if ai_is_useful(text, keyword):
            filtered_rows.append(row)
    
    return pd.DataFrame(filtered_rows)

def main():
    keyword = input("Enter keyword to verify relevance: ").strip()

    twitter_df = filter_file("data/twitter_data.csv", keyword)
    reddit_df = filter_file("data/reddit_data.csv", keyword)

    filtered = pd.concat([twitter_df, reddit_df], ignore_index=True)
    if not filtered.empty:
        os.makedirs("data", exist_ok=True)
        filtered.to_csv("data/filtered_data.csv", index=False)
        print(f"Saved {len(filtered)} filtered posts to data/filtered_data.csv")
    else:
        print("No relevant posts found.")

if __name__ == "__main__":
    main()
