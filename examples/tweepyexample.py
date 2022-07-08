import tweepy

client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAMpRdwEAAAAA7h%2Be9KjiQQXZ0HmMUQbPKuVnY98%3DOERTS2NE1R9J80bWByhj168Z1FEjG4SS9sMpP6tKGq7jwInJIE')


# Gets tweets from steefvanwooning
id = '2374076152'

tweets = client.get_users_tweets(id=id, tweet_fields=['context_annotations','created_at','geo'])

for tweet in tweets.data:
    print(tweet)