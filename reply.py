import sys
import csv
from twitter_utils import get_likers, get_retweeters, reply_to_tweet, send_msg_to_user, get_last_tweet_id
import math
from creds import BOT_USERNAME

WRONG_PARAM = (
    "Zły parametr. Dostępne opcje:"
    "\n\tlikes - konta co polubiły tweet"
    "\n\tretweets - konta co retweetowały tweet"
    "\n\tall - konta co polubiły lub retweetowały tweet."
)


def get_input():
    # opens input file and reads urls
    with open("input.csv", "r") as input:
        inputreader = csv.reader(input)
        jobs = []
        for index, row in enumerate(inputreader):
            # skips first row with column names
            if index == 0:
                continue
            # get number to msg to send
            msg_count = int(row[1])
            msgs = []
            for i in range(msg_count):
                msgs.append(row[2+i])
            jobs.append((row[0], msgs))
        return jobs

def send_msgs(usernames, msg):
    if len(msg) == 1:
        print("1 msg to send")
        for username in usernames:
            print(f"Replying to user: {username}")
            send_msg_to_user(f"@{username}, {msg[0]}")
    else:
        print(f"{len(msg)} msgs to send")
        for username in usernames:
            for index, m in enumerate(msg):
                # check if username or botname is longer to save characters for screename
                if (index == 0):
                    # if 1st part of msg tag username
                    send_msg_to_user(f"@{username}, {m}")
                else:
                    # if not 1st part, reply to previous bot msg
                    tweet_id = get_last_tweet_id()
                    reply_to_tweet(f"{m}", tweet_id)


def main():
    # check shell params. If none given, prints out error msg and kills program
    if len(sys.argv) == 1:
        print(WRONG_PARAM)
        sys.exit()

    # get shell params
    param = sys.argv[1]

    # gets urls from input file
    jobs = get_input()

    if param == "likes":
        # for each url from input file gets likers and sends public msg to them
        for job in jobs:
            likers = get_likers(job[0])
            send_msgs(likers, job[1])

    elif param == "retweets":
        # for each url from input file gets retweeters and sends public msg to them
        for job in jobs:
            retweeters = get_retweeters(job[0])
            send_msgs(retweeters, job[1])

    elif param == "all":
        # for each url from input file gets likers and retweeters and sends public msg to them
        for job in jobs:
            likers = get_likers(job[0])
            send_msgs(likers, job[1])
            retweeters = get_retweeters(job[0])
            send_msgs(retweeters, job[1])

    else:
        print(WRONG_PARAM)


if __name__ == "__main__":
    main()   
    