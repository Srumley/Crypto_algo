import tweepy

def get_twitter_data():
    # Vos clés API Twitter
    consumer_key = 'your_consumer_key'
    consumer_secret = 'your_consumer_secret'
    access_token = 'your_access_token'
    access_token_secret = 'your_access_token_secret'

    # Authentification
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Recherche de tweets
    query = "#bitcoin"
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", since="2021-01-01").items(100)
    tweet_data = [[tweet.created_at, tweet.text] for tweet in tweets]
    df_tweets = pd.DataFrame(tweet_data, columns=["Date", "Tweet"])
    print(df_tweets.head())

    return get_twitter_data