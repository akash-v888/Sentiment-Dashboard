
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time

KEYWORD = "OpenAI"
NUM_TWEETS = 30

async def scrape_tweets():
    tweets = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path="/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary")
        context = await browser.new_context()
        page = await context.new_page()

        search_url = f"https://twitter.com/search?q={KEYWORD}&src=typed_query&f=live"
        await page.goto(search_url)

        # Simulate scrolling to load more tweets
        for _ in range(5):
            await page.mouse.wheel(0, 3000)
            time.sleep(1)

        html = await page.content()
        await browser.close()

        soup = BeautifulSoup(html, 'lxml')
        tweet_divs = soup.find_all('div', attrs={'data-testid': 'tweet'})

        for div in tweet_divs[:NUM_TWEETS]:
            content = div.get_text(separator=' ').strip()
            tweets.append(content)

    # Save to CSV
    df = pd.DataFrame(tweets, columns=["Tweet"])
    df.to_csv("data/twitter_data.csv", index=False)
    print(f"Saved {len(tweets)} tweets to data/twitter_data.csv")

if __name__ == "__main__":
    asyncio.run(scrape_tweets())