# Score attribution based on spam likelyness
unique_times = []
unique_sec = []

# Not used for now but copied from levenstein.py
classification = {
    "none": 0,
    "unlikely": 10,
    "medium": 20,
    "high": 30,
    "spam": 40,
}

# V1 just checks exact same hour/minute combination
# Also for seconds but unsure how accurate that is
def tweet_time_calc(tweetlist):
    duplicate_minutes = 0
    duplicate_seconds = 0
    for tweet in tweetlist:
        date_obj = tweet.created_at
        day = date_obj.day

        minute_obj = [date_obj.hour, date_obj.minute]
        second_obj = [date_obj.hour, date_obj.minute, date_obj.second]

        if minute_obj in unique_times:
            duplicate_minutes +=1

        if second_obj in unique_sec:
            duplicate_seconds += 1

       
        unique_times.append(minute_obj)
        unique_sec.append(second_obj)

    

    score = duplicate_minutes - duplicate_seconds
    score += 10 * duplicate_seconds


    # TODO CLassification
    return score


