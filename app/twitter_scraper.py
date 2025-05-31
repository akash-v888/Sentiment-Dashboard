from playwright.async_api import async_playwright
import asyncio
import re
import pandas as pd
from langdetect import detect
import emoji
import openai
import os
from dotenv import load_dotenv

load_dotenv()
USE_AI_FILTER = False  # Setting true uses OpenAI API
openai.api_key = os.getenv("OPENAI_SECRET")

def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = emoji.replace_emoji(text, replace='')
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def is_valid_tweet(text):
    try:
        if detect(text) != "en":
            return False
    except:
        return False
    text = clean_text(text)
    return len(text) >= 20 and not text.lower().startswith("rt ")

async def ai_is_useful(text, keyword):
    try:
        prompt = f"""You are analyzing tweets from a Twitter search for the keyword: "{keyword}".
Determine if this tweet is relevant and useful for analyzing public sentiment *about* the keyword. 
Respond ONLY with YES or NO.

Tweet:
{text}
"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # gpt-4.0 also works
            messages=[
                {"role": "system", "content": "You evaluate whether tweets are relevant to a topic for sentiment analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        reply = response['choices'][0]['message']['content'].strip().upper()
        return reply.startswith("YES")
    except:
        return False

async def scrape_tweets(keyword="OpenAI", max_tweets=10):
    user_data_dir = "/Users/aviswa/Desktop/Projects/Sentiment-Dashboard/playwright_profile"

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            executable_path="/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"
        )
        page = await browser.new_page()

        search_url = f"https://twitter.com/search?q={keyword}&f=live"
        await page.goto(search_url)
        await page.wait_for_selector('article div[lang]', timeout=15000)

        tweets_data = []
        seen_texts = set()
        scrolls = 0

        while len(tweets_data) < max_tweets and scrolls < 10:
            tweets = await page.query_selector_all('article')

            for tweet in tweets:
                try:
                    content = await tweet.query_selector('div[lang]')
                    raw_text = await content.inner_text()

                    if raw_text in seen_texts:
                        continue
                    seen_texts.add(raw_text)

                    cleaned = clean_text(raw_text)
                    if not is_valid_tweet(cleaned):
                        continue

                    if USE_AI_FILTER:
                        useful = await ai_is_useful(cleaned, keyword)
                        if not useful:
                            continue

                    user_handle = await tweet.query_selector('div[dir="ltr"] span')
                    username = await user_handle.inner_text() if user_handle else "N/A"

                    timestamp_elem = await tweet.query_selector('time')
                    timestamp = await timestamp_elem.get_attribute("datetime") if timestamp_elem else "N/A"

                    tweets_data.append({
                        "text": cleaned,
                        "user": username,
                        "timestamp": timestamp
                    })

                    if len(tweets_data) >= max_tweets:
                        break
                except:
                    continue

            await page.mouse.wheel(0, 3000)
            await asyncio.sleep(2)
            scrolls += 1

        await browser.close()

        df = pd.DataFrame(tweets_data)
        df.to_csv("data/twitter_data.csv", index=False)
        print(f"Scraped and saved {len(df)} cleaned tweets for keyword: '{keyword}'.")

# Entry point with dynamic keyword
if __name__ == "__main__":
    keyword_input = input("Enter a keyword to search tweets for: ").strip()
    asyncio.run(scrape_tweets(keyword=keyword_input))
