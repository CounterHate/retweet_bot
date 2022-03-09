import csv
import creds
import tweepy
import json


def get_input():
    with open("input.csv", "r") as input:
        inputreader = csv.reader(input)
        jobs = []
        for index, row in enumerate(inputreader):
            if index == 0:
                continue
            jobs.append((row[0], row[1]))
        return jobs


def get_user_handle(id):
    auth = tweepy.OAuthHandler(creds.API_KEY, creds.API_KEY_SECRET)
    auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    user = api.get_user(user_id=id)
    return user.screen_name


def get_retweeters(url):
    status_id = url.split("/")[-1]
    # v2
    client = tweepy.Client(creds.BEARER_TOKEN, creds.API_KEY, creds.API_KEY_SECRET)
    retweeters = client.get_retweeters(status_id).data
    for r in retweeters:
        get_user_handle(r.id)
    return retweeters


def send_direct_message(id, msg):
    print(f"sending priv msg to {id}")
    try:
        auth = tweepy.OAuthHandler(creds.API_KEY, creds.API_KEY_SECRET)
        auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        api.send_direct_message(id, msg)
    except:
        raise Exception


def reply_to_tweet(msg, status_id, username):
    # v1.1
    auth = tweepy.OAuthHandler(creds.API_KEY, creds.API_KEY_SECRET)
    auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_status(f"@{username}, {msg}", in_reply_to_status_id=status_id)


def find_retweet(retweeter, tweet_id, tweeter):
    # v1.1
    print("searching for retweet")
    auth = tweepy.OAuthHandler(creds.API_KEY, creds.API_KEY_SECRET)
    auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name=retweeter)
    for t in tweets:
        try:
            if (
                t._json["retweeted_status"]["id_str"] == tweet_id
                and t._json["retweeted_status"]["user"]["screen_name"] == tweeter
            ):
                return t._json
        except Exception as e:
            print(f"Error while searching for retweet: {e}")


def process_job(job, tweet_data):
    retweeters = get_retweeters(job[0])
    for r in retweeters:
        print(f"\n\nReplying to user: {r}")
        try:
            # pass
            send_direct_message(r.id, job[1])
        except Exception:
            tweet = find_retweet(
                retweeter=r, tweet_id=tweet_data["id"], tweeter=tweet_data["username"]
            )
            reply_to_tweet(
                msg=job[1],
                status_id=tweet["id"],
                tweeter=tweet_data["username"],
                retweeter=r,
            )


def get_original_tweet_id_and_username(url):
    data = url.split("/")
    return {"username": data[-3], "id": data[-1]}


def main():
    jobs = get_input()
    for job in jobs:
        tweet_data = get_original_tweet_id_and_username(job[0])
        process_job(job, tweet_data)


if __name__ == "__main__":
    main()
