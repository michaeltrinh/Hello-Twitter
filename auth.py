import twitter
import fileinput
import constants

token_file=fileinput.input("my_keys.txt")


def evaluate_common_ppl_followed(user, friendUser):
    print ("Looking for people you both follow..")
    user_follows = api.GetFriendIDs(user_id=user.GetId(), screen_name=user.GetScreenName())
    print("%s follows %d people." % (user.GetScreenName(), len(user_follows)))

    friend_user_follows = api.GetFriendIDs(user_id=friendUser.GetId(), screen_name=friendUser.GetScreenName())
    print("%s follows %d people." %(friendUser.GetScreenName(), len(friend_user_follows)))

    common_follows = [followerId for followerId in user_follows if followerId in friend_user_follows]

    if len(common_follows) > 0:
        print ("You both follow %d common people." % len(common_follows))

        if raw_input("See common followers names? (y/n) : ") == 'y':
            for commonPersonId in common_follows:
                print("------ ----- ***** ----- -----")
                print("ScreenName: %s" % api.GetUser(user_id=commonPersonId).GetScreenName())
    else:
        print ("You don't follow anyone in common")

def get_user_mentions(fromUser, toUser):
    url = '%s/statuses/user_timeline.json?count=3200&trim_user=1&exclude_replies=0&include_rts=1&screen_name=%s' % \
          (api.base_url,fromUser.GetScreenName())

    json = api._RequestUrl(url, 'GET')
    data = api._ParseAndCheckTwitter(json.content)

    tweets_with_friend_mention = []

    for tweet in data:
        user_mentions = tweet['entities']['user_mentions']
        if user_mentions:
            for user in user_mentions:
                if user['id'] == toUser.GetId():
                    tweets_with_friend_mention.append(tweet)

    print ("In the last 3200 tweets, number of tweets with %s's mention %d" %(toUser.GetScreenName(), len(tweets_with_friend_mention)))
    print ("Tweets:")
    print ("\t----- ----- ***** ----- -----")
    for tweet in tweets_with_friend_mention:
        print ("\t%s" % tweet['text'])
    print ("\t----- ----- ***** ----- -----")


def print_user_details(user):
    print ("***** User stats *****")
    print ("Name            : %s" % user.GetName())
    print ("Description     : %s" % user.GetDescription())
    print ("Follower Count  : %d" % user.GetFollowersCount())
    print ("Following Count : %d" % user.GetFriendsCount())
    print ("User ID         : %d" % user.GetId())

for line in token_file:
    if constants.ACCESS_TOKEN_SECRET in line:
        access_token_secret = line.split(":")[1].strip()
    elif constants.ACCESS_TOKEN in line:
        access_token_key = line.split(":")[1].strip()
    elif constants.CONSUMER_SECRET in line:
        consumer_secret = line.split(":")[1].strip()
    elif constants.CONSUMER_KEY in line:
        consumer_key = line.split(":")[1].strip()

api = twitter.Api(consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret)

user = api.GetUser(screen_name='ankurdh')

print_user_details(user)

friendScreenName = raw_input("Want to do some stats with a friend? Enter friends screen name: ")
print ("Looking for a '%s'...." %friendScreenName)
friendUser = api.GetUser(screen_name=friendScreenName)
print ("Done Looking...")
if user:
    print_user_details(friendUser)
else:
    print ("User '%s' not found." %friendScreenName)

get_user_mentions(user, friendUser)

evaluate_common_ppl_followed(user, friendUser)

print ("Looking for common followers..")
userFollowers = api.GetFollowerIDs(user_id=user.GetId(), screen_name=user.GetScreenName())
friendUserFollowers = api.GetFollowerIDs(user_id=friendUser.GetId(), screen_name=friendUser.GetScreenName())

print ("%s is followed by %d people" %(user.GetScreenName(),len(userFollowers)))
print ("%s is followed by %d people" %(friendUser.GetScreenName(),len(friendUserFollowers)))

commonFollowers = [followerId for followerId in userFollowers if followerId in friendUserFollowers]

if len(commonFollowers) > 0:
    print ("You both have %d common followers." % len(commonFollowers))

    if raw_input("See common followers names? (y/n) : ") == 'y':
        for commonPerson in commonFollowers:
            print("------ ----- ***** ----- -----")
            print("ScreenName: %s" % api.GetUser(user_id=commonPerson).GetScreenName())

else:
    print ("You don't have common followers..")
