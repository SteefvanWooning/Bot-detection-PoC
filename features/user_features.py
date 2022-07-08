import access
from datetime import datetime, date, timezone, timedelta

# TODO add more spam likely strings
spam_list = ['spam', 'bot', 'xxx', 'free', ]
spam_score = {
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

# these functions extract the required data from the twitter user data
def protected_check(user_data):
    return user_data['protected']

def follow_ratio(user_data):
    if user_data['public_metrics']['followers_count'] == 0:
        return 0
    return user_data['public_metrics']['following_count']/user_data['public_metrics']['followers_count']

# checks the ratio of verified to non-verified follows on a certain account
# arguments: list of accounts the main account is following and the amount of follows 
def verified_follow(following, follow_amount):
    verified_count = 0
    for account in following:
        if access.get_user_object(account.id)['verified']:
            verified_count += 1
    # threshold at 65% of following users verified?
    if verified_count/follow_amount >= 0.65:
        return True
    return False

# obtain the age of the account. Pay attention to the date format
def account_age(user_data):
    today = date.today()
    desc_score = description(user_data)
    creation_date = datetime.strptime(user_data['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ").date() # the created_at date includes uncessesary information; we only require the date
    return (creation_date-today).days * -1

# extract and analyze the profile picture of an account
# mainly a check if the image matches the default one
def picture_check(user_data):
    default_image = "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png"
    return (user_data['profile_image_url'] == default_image)

# Checks to see if the account is verified.
# If yes this indicate an extreme likeliness the account is not a bot.
def verified(user_data):
    return user_data['verified']


# This function checks if the username contains spam substrings.
def name_check(user_data):
    score = 0
    username = user_data["username"]
    for spam_string in spam_list:
        if spam_string in username:
            score += 10

    return score
    

# This function checks if the name contains spam substrings.
# Function could be merged with name_check.
def user_check(user_data):
    score = 0
    name = user_data["name"]
    for spam_string in spam_list:
        if spam_string in name:
            score += 10
   
    return score
    

# Function to check description of the account.
# It focusses both on length and spampatterns
# TODO check spam strings in description
def description(user_data):
    score = 0
    desc = user_data["description"]
    
    # See if description is empty, bots are more likely
    # to have empty or single character descriptions.
    # Arbitrary value set.
    if len(desc) < 15:
        score += 30

    for spam_string in spam_list:
        if spam_string in desc:
            score += 10
   
    return score
    

def get_statistics(user_data, user_id):
    verify = verified(user_data)
    name_score = name_check(user_data)
    user_score = user_check(user_data)
    desc_score = description(user_data)

    total = name_score + user_score + desc_score
    # maximum score
    if total > 80:
        total = 80

    if(verify):
        total -= 80

    likeliness = spam_score[str(total)]

    # TODO integrate dannys part
    age = account_age(user_data)
    

    return [verify, name_score, user_score, desc_score, likeliness]
