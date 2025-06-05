# Sentiment Dashboard

This repository contains a small collection of scripts for scraping Reddit and Twitter content with the goal of building a sentiment-analysis dashboard. The project is still in an early stage: the Streamlit dashboard and sentiment analysis module are stubs, but the scrapers can already collect data into CSV files.

## Repository Layout

```
app/
  reddit_scraper.py    - Collects posts from specified subreddits via the Reddit API.
  twitter_scraper.py   - Uses Playwright to scrape tweets from Twitter search results.
  scraper.py           - Example of combining both scrapers (not fully implemented).
  signin_script.py     - Helper script to create a logged-in Playwright profile for Twitter.
  sentiment.py         - Placeholder for future sentiment-analysis logic.

dashboard/
  streamlit_app.py     - Placeholder for the Streamlit dashboard.

requirements.txt       - Python dependencies.
```

## Setup

1. **Python**: Install Python 3.10 or newer.
2. **Virtual Environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**: Create a `.env` file in the project root containing credentials for Reddit and optional OpenAI access:

   ```text
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USERNAME=your_username
   REDDIT_PASSWORD=your_password
   REDDIT_USER_AGENT=sentiment-dashboard

   OPENAI_SECRET=sk-...
   ```

   The Twitter scraper expects an already signed-in browser profile. The `signin_script.py` file launches a persistent Playwright context so you can log in manually.

## Usage

### Reddit Scraper

Fetches recent posts containing a keyword across several subreddits and writes them to `data/reddit_data.csv`.

```bash
python app/reddit_scraper.py
```
You will be prompted for a keyword.

### Twitter Scraper

Scrapes live tweets for a keyword using Playwright. Update `user_data_dir` and `executable_path` in `twitter_scraper.py` to match your system. Results are written to `data/twitter_data.csv`.

```bash
python app/twitter_scraper.py
```

To optionally filter tweets with OpenAI, set `USE_AI_FILTER = True` in the script and provide `OPENAI_SECRET` in your `.env` file.

### Dashboard

`dashboard/streamlit_app.py` is a placeholder. Once implemented you will be able to run it with:

```bash
streamlit run dashboard/streamlit_app.py
```

## Notes

- The repository currently contains no sentiment analysis or visualization code; these parts are for future development.
- Data files are written to a `data/` directory, which is ignored by Git (`.gitignore`).

