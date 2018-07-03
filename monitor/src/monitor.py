from datetime import datetime
import logging
import pprint
import re
import time

import praw

def main():
    print("STARTING")

    reddit = praw.Reddit(
        client_id=,
        client_secret=,
        username=,
        password=,
        user_agent=
    )

    while True:
        now = datetime.now()
        for s in reddit.subreddit("memeeconomy").new(limit=None):
            print(f"{now}\t{s.id}\t{s.created_utc}\t{s.ups}\t{s.score}")
        time.sleep(600)

if __name__ == "__main__":
    main()
