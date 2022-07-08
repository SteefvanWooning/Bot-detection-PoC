import json

def calulcate_entities(tweetlist):
    ht, url, mentions = 0, 0, 0
    for tweet in tweetlist:
        entities = tweet.entities

        if entities != None:

            if "hashtags" in entities.keys():
                ht += len(entities["hashtags"])
            if "urls" in entities.keys():
                url += len(entities["urls"])
            if "mentions" in entities.keys():
                mentions += len(entities["mentions"])

    prcent_ht = (ht / len(tweetlist)) * 100
    prcent_mt = (mentions / len(tweetlist)) * 100
    prcent_url = (url / len(tweetlist)) * 100

                
    print("Amount of hashtags in tweets: " + str(ht) + " > " + str(prcent_ht) +"%")
    print("Amount of urls in tweet: " + str(url) + " > " + str(prcent_url) +"%")
    print("Amount of mentions in tweet: " + str(mentions)+ " > " + str(prcent_mt) +"%")

    print("Amount of tweets: " + str(len(tweetlist)))

    # Return values are in the shape of 3 list items containing count and percentage.
    result_list = [[ht, prcent_ht], [url, prcent_url], [mentions, prcent_mt]]
    return result_list
