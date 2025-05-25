# app/test_reddit.py
import praw

reddit = praw.Reddit(
    client_id="l6V0G-WG0T1n7kHDhmmW9w",
    client_secret="uRc1GFf_qCg_lDoJtYconsAJB9xhJQ",
    password="akashviswanathan",
    user_agent="sentiment-dashboard-script by /u/sentiment-analyst-bo",
    username="sentiment-analyst-bo"
)

print(reddit.read_only)
print(reddit.user.me())
