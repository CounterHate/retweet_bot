import creds
import tweepy
import json


def get_retweeters(url):
    status_id = url.split("/")[-1]
    # v2
    client = tweepy.Client(creds.BEARER_TOKEN, creds.API_KEY, creds.API_KEY_SECRET)
    data = client.get_retweeters(status_id).data
    retweeters = []
    for r in data:
        retweeters.append(get_user_handle(r.id))
    return retweeters

def get_last_tweet_id():
    # v2
    # client = tweepy.Client(creds.BEARER_TOKEN, creds.API_KEY, creds.API_KEY_SECRET)
    # data = client.get_users_tweets(id="botWojownicy", max_results=1)
    # print("last result: ", data)
    # v1.1
    auth = tweepy.OAuthHandler(creds.API_KEY, creds.API_KEY_SECRET)
    auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    tweets = api.user_timeline(count=1)
    return tweets[0].id

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


def get_likers(url):
    status_id = url.split("/")[-1]
    # v2
    client = tweepy.Client(creds.BEARER_TOKEN, creds.API_KEY, creds.API_KEY_SECRET)
    data = client.get_liking_users(status_id).data
    likers = []
    for l in data:
        likers.append(get_user_handle(l.id))
    return likers


def get_user_handle(id):
    auth = tweepy.OAuthHandler(creds.API_KEY, creds.API_KEY_SECRET)
    auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    user = api.get_user(user_id=id)
    return user.screen_name


def get_status(id):
    auth = tweepy.OAuthHandler(creds.API_KEY, creds.API_KEY_SECRET)
    auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    status = api.get_status(id)
    print(status.user)


def send_direct_message(id, msg):
    auth = tweepy.OAuthHandler(creds.API_KEY, creds.API_KEY_SECRET)
    auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.send_direct_message(id, msg)


def send_msg_to_user(msg):
    # v1.1
    auth = tweepy.OAuthHandler(creds.API_KEY, creds.API_KEY_SECRET)
    auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_status(msg)


def reply_to_tweet(msg, status_id):
    # v2
    # client = tweepy.Client(creds.BEARER_TOKEN, creds.API_KEY, creds.API_KEY_SECRET)
    # client.create_tweet(text=msg, quote_tweet_id=status_id)
    # v1.1
    auth = tweepy.OAuthHandler(creds.API_KEY, creds.API_KEY_SECRET)
    auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_status(msg, in_reply_to_status_id=int(status_id))


def get_timeline(username):
    # v1.1
    auth = tweepy.OAuthHandler(creds.API_KEY, creds.API_KEY_SECRET)
    auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name=username)
    for t in tweets:
        print(json.dumps(t._json, indent=2))


def get_retweets(url):
    # v1.1
    auth = tweepy.OAuthHandler(creds.API_KEY, creds.API_KEY_SECRET)
    auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    retweets = api.get_retweets(url.split("/")[-1])
    for t in retweets:
        print(json.dumps(t._json, indent=2))


def main():
    pass
    # get_retweeters("https://twitter.com/BrewysTable/status/1477293541126598656")
    # get_status('1473215909561044994')
    # send_direct_message('161998880', 'Elo')
    # reply_to_tweet("@edekgb YAY", "1500828731165876230")
    # get_timeline("pawelkorpal")
    # get_retweets("https://twitter.com/mjbroniarz/status/1486590015656316929")
    # get_last_tweet_id()

if __name__ == "__main__":
    main()
