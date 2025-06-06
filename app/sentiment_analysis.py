import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    """Returns compound sentiment score from -1 (neg) to 1 (pos)."""
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)["compound"]

def label_sentiment(score):
    """Convert numeric score to sentiment label."""
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def main():
    input_path = "data/filtered_data.csv"
    output_path = "data/sentiment_data.csv"

    if not os.path.exists(input_path):
        print(f"[!] File not found: {input_path}")
        return

    df = pd.read_csv(input_path)
    if "text" not in df.columns:
        print("[!] 'text' column missing in input file.")
        return

    # Apply sentiment analysis
    print(f"Analyzing sentiment of {len(df)} posts...")
    df["sentiment_score"] = df["text"].apply(analyze_sentiment)
    df["sentiment_label"] = df["sentiment_score"].apply(label_sentiment)

    # Save results
    os.makedirs("data", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Sentiment data saved to {output_path}")

if __name__ == "__main__":
    main()
