import pandas as pd
import os
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    """
    Lowercase, remove URLs, mentions, punctuation, and extra whitespace.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|@\w+|#\w+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text

def relevance_score(text, keyword):
    """
    Calculate cosine similarity between keyword and post.
    """
    try:
        docs = [clean_text(keyword), clean_text(text)]
        tfidf = TfidfVectorizer().fit_transform(docs)
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return score
    except Exception:
        return 0.0

def filter_file(path, keyword, threshold=0.1):
    """
    Filter rows in CSV file by relevance and log excluded posts.
    """
    if not os.path.exists(path):
        print(f"[!] File not found: {path}")
        return pd.DataFrame()
    
    df = pd.read_csv(path)
    if "text" not in df.columns:
        print(f"[!] 'text' column missing in {path}")
        return pd.DataFrame()
    
    filtered_rows = []
    excluded_log = []

    for _, row in df.iterrows():
        text = row.get("text", "")
        score = relevance_score(text, keyword)
        row["relevance_score"] = score

        if score >= threshold:
            filtered_rows.append(row)
        else:
            excluded_log.append((text[:80], score))  # Preview + score

    print(f"\n[LOG] Skipped {len(excluded_log)} posts below threshold ({threshold}):")
    for preview, score in excluded_log[:10]:
        print(f"  ({score:.2f}) {preview}...")

    return pd.DataFrame(filtered_rows)

def main():
    keyword = input("Enter keyword to verify relevance: ").strip()
    
    twitter_df = filter_file("data/twitter_data.csv", keyword)
    reddit_df = filter_file("data/reddit_data.csv", keyword)

    combined = pd.concat([twitter_df, reddit_df], ignore_index=True)
    if not combined.empty:
        os.makedirs("data", exist_ok=True)
        combined.to_csv("data/filtered_data.csv", index=False)
        print(f"\nSaved {len(combined)} filtered posts to data/filtered_data.csv")
    else:
        print("\n[!] No relevant posts found.")

if __name__ == "__main__":
    main()
