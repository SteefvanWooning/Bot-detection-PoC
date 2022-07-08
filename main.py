import cli
import sys
import access
import csv
import json
import time
from datetime import datetime, date, timezone, timedelta
import features.tweet_features
import features.user_features
import features.levenstein
import features.chi_square
import features.entity_pt
from features.levenstein import calculate_distance
from features.tweet_timing import tweet_time_calc

def main():
    cli_obj = cli.cli_parser(sys.argv[1], sys.argv[2])
    # use the first cli argument as user_id for now
    user_id = sys.argv[1]
    user_data = obtain_user(user_id)

    # user_check(user_data)

    # select_accounts('bot', amount=100)

    account_check('bot_ids.txt')
    # account_check('human_ids.txt')

    # print(features.user_features.picture_check(user_data))
    # tweet_list = access.get_tweet_list(user_id, amount=100, fields='created_at,geo,source')
    # tweet_list = access.big_tweet_list(user_id, page_amount=5, fields='created_at')
    
    # features.chi_square.chi_square(tweet_list)
    # print(tweet_list) 
    # [print(tweet.created_at) for tweet in tweet_list]

    # is the account protected? If so, probably not authentic, exit
    # if(features.user_features.protected_check(user_data)):
    #     print("Account is protected, quitting.")
    #     exit()

    # features.tweet_features.source_score(tweet_list)
    # features.tweet_features.geo_score(tweet_list)

    # calculate the rate of followers to following
    # follower_ratio = features.user_features.follow_ratio(user_data)
    # print(f"Follow ratio: {follower_ratio}")

    # obtain the age of the account in days
    # age = features.user_features.account_age(user_data)
    # print(f"Account age in days: {age}")

    # print(f"Average Tweet length: {features.tweet_features.average_tweet_length(tweet_list)}")

    # print(f"Average Tweet Rate: {features.tweet_features.tweet_rate(tweet_list)}")

    # for now we try to access all the accounts a target is following
    # following = access.get_following(user_id, user_data['public_metrics']['following_count'])
    
    # the following check can take a while, to test it quickly use a smaller amount of followers to retreive
    # following = access.get_following(user_id, amount=130)
    # print(f"Do we hit the verified threshold?: {features.user_features.verified_follow(following, user_data['public_metrics']['following_count'])}")

    # Levenstein distance calculation test
    # identical_tweet_score = features.levenstein.calculate_distance(tweet_list)
    # print(f"Score based on likeliness of spam tweets: {str(identical_tweet_score)}")

    # Timing precision calculation test
    # timing_score = tweet_time_calc(tweet_list)
    # print("Score based on likeliness of tweet timing: " + str(timing_score))
    # features.entity_pt.calulcate_entities(tweet_list)
    # user_stats = features.user_features.get_statistics(user_data, user_id)
    # verify, name_score, user_score, desc_score, like = user_stats
    # TODO publish on the webapp
    # print("Account is verified: " + str(verify))
    # print("String spam patterns are in the username: " + str(user_score))
    # print("String spam patterns are in the name: " + str(name_score))
    # print("Description score: " + str(desc_score))
    # print("Likeliness based on these statistics: " +str(like)) 

    

# obtain the user object corresponding to the user ID
def obtain_user(user_id):
    return access.get_user_object(user_id=user_id)

# entry for the webserver
def entrypoint(handle):
    values = {}

    # user_id = arg
    user_data = access.get_user_id(handle)
    user_id = user_data["id"]
    tweet_list = access.get_tweet_list(user_id, amount=5, fields='created_at')
   

    default_picture = features.user_features.picture_check(user_data)
    values["Is the default profile picture used?"] = default_picture

    # Levenstein distance calculation test
    identical_tweet_score = calculate_distance(tweet_list)
    values["Identical Tweet Test"] = identical_tweet_score

    # Test to determine if tweets are sent on a precise interval
    timing_score = tweet_time_calc(tweet_list)
    values["Similar Timing test"] = timing_score

    entity_count = features.entity_pt.calculate_entities(tweet_list)
    ht, ht_prcnt = entity_count[0]
    url, url_prcnt = entity_count[1]
    ment, mnt_prcnt = entity_count[2]
    # TODO put in values however wanted



    sourced_tweets = features.tweet_features.source_score(tweet_list)
    geo_tagged = features.tweet_features.geo_score(tweet_list)

    values["Amount of Tweets with a source"] = sourced_tweets
    values["Amount of geo tagged Tweets"] = geo_tagged

    # calculate the rate of followers to following
    follower_ratio = features.user_features.follow_ratio(user_data)
    values["Following to follow ratio"] = follower_ratio

    #  obtain the age of the account in days
    age = features.user_features.account_age(user_data)
    
    values["Account age (in days)"] = age

    average_length = features.tweet_features.average_tweet_length(tweet_list)

    values["Average Tweet length"] = average_length

    tweet_rate = features.tweet_features.tweet_rate(tweet_list)

    values["Tweets per hour (24h average)"] = tweet_rate

    # for now we try to access all the accounts a target is following
    # following = access.get_following(user_id, user_data['public_metrics']['following_count'])
    
    # the following check can take a while, to test it quickly use a smaller amount of followers to retreive
    following = access.get_following(user_id, amount=130)
    verified_threshold = features.user_features.verified_follow(following, user_data['public_metrics']['following_count'])

    values["Does this account follow more than 65% verified accounts?"] = verified_threshold


    return values


def user_check(user_data):

    user_json = {}

    tweet_list = access.get_tweet_list(user_data['id'], amount=100, fields='created_at,geo,source')
    
    user_json['id'] = user_data['id']
    user_json['age'] = features.user_features.account_age(user_data)
    user_json['verified'] = features.user_features.verified(user_data)
    user_json['protected'] = features.user_features.protected_check(user_data)

    user_json['name_check'] = features.user_features.name_check(user_data)
    user_json['user_check'] = features.user_features.user_check(user_data)
    user_json['description'] =  features.user_features.description(user_data)    
    user_json['default_pic'] = features.user_features.picture_check(user_data)
    user_json['follower_ratio'] = features.user_features.follow_ratio(user_data)
    
    if(features.user_features.protected_check(user_data)):
        sleep(900)
        return user_json

    # the following check can take a while, to test it quickly use a smaller amount of followers to retreive
    following = access.get_following(user_data['id'], amount=280)
    user_json['verified_threshold'] = features.user_features.verified_follow(following, user_data['public_metrics']['following_count'])
        
    user_json['geo'] = features.tweet_features.geo_score(tweet_list)
    user_json['source'] = features.tweet_features.source_score(tweet_list)
    user_json['avg_tweet'] = features.tweet_features.average_tweet_length(tweet_list)
    user_json['tweet_rate'] = features.tweet_features.tweet_rate(tweet_list)
    user_json['timing_score'] = tweet_time_calc(tweet_list)
    user_json['identical_tweet_score'] = features.levenstein.calculate_distance(tweet_list)

    return user_json

# select 20 accounts from the twibot-22 dataset; select either 'bot' or 'human'
def select_accounts(selection='bot', amount = 20):
    file_name = "label.csv"

    accounts = []

    with open(file_name, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if(row[1] == selection and len(accounts) < amount):
                print(row[0][1:])
                accounts.append(row[0][1:])

# run tests on the IDs found in the file, save this in JSON format          
def account_check(file_name):
    with open(file_name, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                print(row)
                user_data = access.get_user_object(row[0])
                json_string = user_check(user_data)
                print(json_string)
                with open('score_data.json', 'a', newline='\n') as outfile:
                    json.dump(json_string, outfile)
                    outfile.write('\n')

                time.sleep(900) # sleep for 15 minutes, to not hit the API cap
            except Exception as e:
                print(e)
                print(f"Something went wrong with ID: {row}")

# calculate the average scores for the different tests
def twibot_tests():
    pass

if __name__ == "__main__":
    main()
