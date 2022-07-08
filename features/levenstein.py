import itertools

# Score attribution based on spam likelyness
classification = {
    "0": "No indication",
    "10": "Very unlikely",
    "20": "Unlikely",
    "30": "Average",
    "40": "Indecisive",
    "50": "Somewhat likely",
    "60": "Likely",
    "70": "Very Likely",
    "80": "Extremely likely"

}

distances = []

def loop_tweets(tweet_x, tweet_y):
    longer = max(len(tweet_x), len(tweet_y))
    distance = 0
    for i in range(0,longer):
        # If tweet is done
        if i > len(tweet_x)- 1 or i > len(tweet_y) - 1:
            break
        else:
            # Compare char
            if tweet_x[i] != tweet_y[i]:
                distance += 1
            
    return distance


def calculate_distance(tweetlist):

    combinations = list(itertools.combinations(range(0, len(tweetlist)), r=2))
    for x, y in combinations:
        distances.append(loop_tweets(str(tweetlist[x]), str(tweetlist[y])))


    # # Go through all tweets row-wise
    # for x in range(0, len(tweetlist)):
    #     # Go through all tweets columnwise
    #     for y in range(0,len(tweetlist)):
    #         if tweetlist[x].id == tweetlist[y].id:
    #             continue
    #         else:
    #             distances.append(loop_tweets(str(tweetlist[x]), str(tweetlist[y])))


    # Get the values of the set
    identicals = 0
    similars = 0
    mediums = 0

    for value in distances:
        if value < 11:
            identicals += 1
        if value < 20 and value >  10:
            similars += 1
        if value < 30 and value > 20:
            mediums += 1

    # score appointment can be tweaked:
    score = 2 * identicals + 1.5 * similars + 1 * mediums

    if score > 0.8 * len(tweetlist):
        return classification["10"]
    elif score > 0.6 * len(tweetlist):
        return classification["30"]
    elif score > 0.4 * len(tweetlist):
        return classification["50"]
    elif score > 0.2 * len(tweetlist):
        return classification["70"]
    else:
        return classification["0"]


