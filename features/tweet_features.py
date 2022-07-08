from datetime import datetime, date, timezone, timedelta

# these functions extract the required data from the tweet data
def obtain_source(tweet_data):
    return tweet_data['source']

# analyze the tweets for the existence of tweets with a source
def source_score(tweet_list):
    source_tagged = len([tweet.source for tweet in tweet_list if tweet.source != None])    
    return source_tagged

# analyze the tweets for the existence of a geo tag on the tweets
def geo_score(tweet_list):
    geo_tagged = len([tweet for tweet in tweet_list if tweet.geo != None])
    return geo_tagged

# calculate the length of the average X amount of tweets
# of note, mentions do count towards the length of a tweet
def average_tweet_length(tweet_list):
    list_length = len(tweet_list)
    char_sum = sum([len(text) for text in tweet_list])
    return char_sum / list_length

# calculate the amount of tweets per hour, for the last X amount of days
def tweet_rate(tweet_list, days=1):
    start_from = datetime.now(timezone.utc)-timedelta(days)
    period_tweets = [tweet for tweet in tweet_list if tweet.created_at >= start_from]
    return len(period_tweets)/(24*days) # get the amount of tweets per hour

# calculate the amount of tweets per hour, for the last X amount of days
def tweet_rate(tweet_list, days=1):
    start_from = datetime.now(timezone.utc)-timedelta(days)
    period_tweets = [tweet for tweet in tweet_list if tweet.created_at >= start_from]
    return len(period_tweets)/(24*days) # get the amount of tweets per hour