from playwright.async_api import async_playwright
import asyncio

async def scrape_twitter():
    user_data_dir = "/Users/aviswa/Desktop/Projects/Sentiment-Dashboard/playwright_profile"  # Adjust path as needed

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            executable_path="/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"
        )
        page = await browser.new_page()
        await page.goto("https://twitter.com/search?q=OpenAI&f=live")
        await asyncio.sleep(20)  # give time to load or manually interact if needed
        await browser.close()

asyncio.run(scrape_twitter())
