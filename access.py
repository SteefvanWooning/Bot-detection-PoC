import requests
import os
import json
import tweepy


# this file is to be used for making calls to the API

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

# create the client with the proper access token
client = tweepy.Client(bearer_token)

# in order to not waste API calls, (nearly) all available fields are requested at each call 
all_user_fields = "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
all_tweet_fields = "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld"


# Turn handle into user id.
def get_user_id(handle, fields=None):
    response = client.get_user(username=handle,user_fields=all_user_fields)
    return response.data.data

# obtain the user object belonging to the specified user ID
# generic function; request the proper fields
def get_user_object(user_id, fields=all_user_fields):
    response = client.get_user(id=user_id,user_fields=fields)
    return response.data.data

# obtain the last X amount of tweets placed by the user_id account (including replies)
def get_tweet_list(user_id, amount = 50, start=None, fields=None):
    response = client.get_users_tweets(user_id, max_results=amount, start_time=start, tweet_fields = fields)
    return response.data

# obtain the last 3200 tweets placed by the user_id account (including replies)
def big_tweet_list(user_id, amount = 100, page_amount = 5, fields=None):
    response = client.get_users_tweets(user_id, max_results=amount, tweet_fields = fields)
    tweet_list = response.data
    print(tweet_list)
    print(response)
    next_token = response.meta['next_token']
    for i in range(0,page_amount-1):
        response = client.get_users_tweets(user_id, max_results=amount, pagination_token=next_token,tweet_fields = fields)
        tweet_list += response.data
        next_token = response.meta['next_token']

    print(len(tweet_list))
    return tweet_list

# obtain the tweet object belonging to the specified tweet ID
# generic function; request the proper fields
def get_tweet_object(tweet_id, fields=None):
    response = client.get_tweet(id=tweet_id, tweet_fields=all_tweet_fields)
    return response.data.data

# obtain the list of accounts that are being followed by user_id
# if more than 100 tweets are desired, pagination should be used
def get_following(user_id, amount=100):
    response = client.get_users_following(user_id, max_results=amount)
    return response.data