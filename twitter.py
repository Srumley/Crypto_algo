import tweepy
import pandas as pd
from IPython import embed

def get_twitter_data():


    consumer_key="cNRrzH4zDwnSRbO5l9Kcog4ag"
    consumer_secret="bANuRsDE9BSnCMIeDDW3t6PxwtgsDfARg6PYstduxbD0jbR7DQ"
    access_token="1541812033313718273-mtcqVBxHAHA9mWX5z8XHEz5KrkI3ia"
    access_token_secret="SfimIFNwqIaNdAcAR9bx6MOWOYjnU1aKvGPZ9sgjuDAUk"
    

    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
    

    client = tweepy.Client(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    # Authentification
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Recherche de tweets
    query = "#bitcoin"
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", since="2021-01-01").items(100)
    embed()
    tweet_data = [[tweet.created_at, tweet.text] for tweet in tweets]
    df_tweets = pd.DataFrame(tweet_data, columns=["Date", "Tweet"])
    
   

    return df_tweets