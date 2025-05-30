from playwright.async_api import async_playwright
import asyncio
import time

async def scrape_tweets(keyword="OpenAI", max_tweets=10):
    user_data_dir = "/Users/aviswa/Desktop/Projects/Sentiment-Dashboard/playwright_profile"

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            executable_path="/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"
        )
        page = await browser.new_page()

        # Load Twitter search
        search_url = f"https://twitter.com/search?q={keyword}&f=live"
        await page.goto(search_url)
        await page.wait_for_selector('article div[lang]', timeout=15000)

        tweets_data = []
        last_height = None
        scrolls = 0

        while len(tweets_data) < max_tweets and scrolls < 10:
            tweets = await page.query_selector_all('article')

            for tweet in tweets:
                try:
                    content = await tweet.query_selector('div[lang]')
                    text = await content.inner_text()

                    user_handle = await tweet.query_selector('div[dir="ltr"] span')
                    username = await user_handle.inner_text() if user_handle else "N/A"

                    timestamp_elem = await tweet.query_selector('time')
                    timestamp = await timestamp_elem.get_attribute("datetime") if timestamp_elem else "N/A"

                    tweets_data.append({
                        "text": text,
                        "user": username,
                        "timestamp": timestamp
                    })

                    if len(tweets_data) >= max_tweets:
                        break
                except:
                    continue

            # Scroll to load more
            await page.mouse.wheel(0, 3000)
            await asyncio.sleep(2)
            scrolls += 1

        await browser.close()

        print(f"✅ Scraped {len(tweets_data)} tweets:\n")
        for i, tweet in enumerate(tweets_data):
            print(f"{i+1}. [{tweet['timestamp']}] @{tweet['user']}:\n{tweet['text']}\n")

asyncio.run(scrape_tweets())
