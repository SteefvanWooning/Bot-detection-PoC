from datetime import datetime
from scipy.stats import chisquare

def chi_square(tweet_list):
    hour_frequency = [0]*24
    minute_frequency = [0]*60
    day_frequency = [0]*7

    for tweet in tweet_list:
        creation_date = tweet.created_at
        if(creation_date == None):
            continue

        hour = creation_date.hour
        hour_frequency[hour] += 1

        minute = creation_date.minute
        minute_frequency[minute] += 1 

        day = creation_date.weekday()
        day_frequency[day] += 1

    chi_output = chisquare(hour_frequency)

    chi_output = chisquare(minute_frequency)

    chi_output = chisquare(day_frequency)
    print(day_frequency)
    print(chi_output)