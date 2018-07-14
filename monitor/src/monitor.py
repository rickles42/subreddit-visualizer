from datetime import datetime
import logging
import pprint
import re
import time

import praw

import config

def main():
    print("timestamp\tid\tcreated_utc\tups\tscore")

    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        username=config.username,
        password=config.password,
        user_agent=config.user_agent
    )

    while True:
        now = datetime.now()
        for s in reddit.subreddit("memeeconomy").new(limit=None):
            print(f"{now}\t{s.id}\t{s.created_utc}\t{s.ups}\t{s.score}")
        time.sleep(600)

if __name__ == "__main__":
    main()
