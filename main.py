import json
import tweepy
from flask import Flask

app = Flask(__name__)


def load_keys():
    with open("keys.json") as fp:
        return json.load(fp)

def load_queries():
    with open("queries.json") as fp:
        return json.load(fp)

def process():
    keys = load_keys()
    print keys
    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    api = tweepy.API(auth)

    queries = load_queries()
    print queries

    tweets_per_query  = 50

    new_tweets = 0
    for key in queries:
        for querry in queries[key]: 
            if key == 'people':
                querry = "from:" + querry
                #continue
            #print ("Starting new querry: " + querry)
            for tweet in tweepy.Cursor(api.search, q=querry, tweet_mode="extended").items(tweets_per_query ):

                user = tweet.user.screen_name
                id = tweet.id
                url = 'https://twitter.com/' + user +  '/status/' + str(id)
                print (url)

                try:
                    pass
                    text = tweet.retweeted_status.full_text.lower()
                except:
                    text = tweet.full_text.lower()
                #print text.encode('ascii', 'ignore')
                #print '-'*50
                if "retweet" in text or "rt" in text:
                    if not tweet.retweeted:
                        try:
                            tweet.retweet()
                            #print("\tRetweeted")
                            new_tweets += 1
                        except tweepy.TweepError as e:
                            print('\tAlready Retweeted')

                if "like" in text or "fav" in text:
                    try:
                        tweet.favorite()
                        pass #print('\t' + "Liked")
                    except:pass
                        #print('\tAlready Liked')
                if 0 and "follow" in text:
                    try:
                        to_follow = [tweet.retweeted_status.user.screen_name] + [i['screen_name'] for i in tweet.entities['user_mentions']]
                    # Don't follow origin user (person who retweeted)
                    except:
                        to_follow = [user] + [i['screen_name'] for i in tweet.entities['user_mentions']]

                    for screen_name in list(set(to_follow)):
                        api.create_friendship(screen_name)
                        print('\t' + "Followed: " + screen_name)

        print ("New Tweets: " + str(new_tweets))

if __name__ == "__main__":
    while True:
        process()


