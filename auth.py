import twitter
import fileinput
import constants

file=fileinput.input("my_keys.txt")

for line in file:
    if constants.ACCESS_TOKEN_SECRET in line:
        access_token_secret = line.split(":")[1].strip()
    elif constants.ACCESS_TOKEN in line:
        access_token_key = line.split(":")[1].strip()
    elif constants.CONSUMER_SECRET in line:
        consumer_secret = line.split(":")[1].strip()
    elif constants.CONSUMER_KEY in line:
        consumer_key = line.split(":")[1].strip()

"""print ("Access Token: %s"
       "Access Token Secret: %s"
       "Consumer Key: %s"
       "Consumer Secret: %s"
       %(access_token_key, access_token_secret, consumer_key, consumer_secret))
"""
api = twitter.Api(consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret)

user = api.GetUser(screen_name='ankurdh')

print ("***** User stats *****")
print ("Name            : %s" %user.GetName())
print ("Description     : %s" %user.GetDescription())
print ("Follower Count  : %d" %user.GetFollowersCount())
print ("Following Count : %d" %user.GetFriendsCount())
print ("User ID         : %d" %user.GetId())

print ("***** Recent User Retweets *****")
retweets=api.GetUserRetweets()

for retweet in retweets:
    print retweet.GetText()