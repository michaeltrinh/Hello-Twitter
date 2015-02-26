import twitter
import fileinput
import constants

file=fileinput.input("my_keys.txt")

def printUserDetails(user):
    print ("***** User stats *****")
    print ("Name            : %s" %user.GetName())
    print ("Description     : %s" %user.GetDescription())
    print ("Follower Count  : %d" %user.GetFollowersCount())
    print ("Following Count : %d" %user.GetFriendsCount())
    print ("User ID         : %d" %user.GetId())

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

printUserDetails(user)

friendScreenName = raw_input("Want to do some stats with a friend? Enter friends screen name: ")
print ("Looking for a '%s'...." %friendScreenName)
friendUser = api.GetUser(screen_name=friendScreenName)
print ("Done Looking...")
if user:
    print ("Username: %s, ID: %s" %(friendUser.GetName(),friendUser.GetId()))
else:
    print ("User '%s' not found." %friendScreenName)

printUserDetails(friendUser)

print ("Looking for common followers..")
userFollowers = api.GetFollowers(user_id=user.GetId())
friendUserFollowers = api.GetFollowers(user_id=friendUser.GetId())

commonFollowers = []

for userFollower in userFollowers:
    for friendUserFollower in friendUserFollowers:
        if userFollower.GetId() == friendUserFollower.GetId():
            commonFollowers.append(userFollower)

if len(commonFollowers) > 0:
    print ("You both have %d common followers." % len(commonFollowers))

    if raw_input("See common followers names? (y/n) : ") == 'y':
        for commonPerson in commonFollowers:
            print("------ ----- ***** ----- -----")
            print("ScreenName: %s" % commonPerson.GetScreenName())

else:
    print ("You don't have common followers..")

print ("Looking for people you both follow..")
userFollows = api.GetFriends(user_id=user.GetId())
friendUserFollows = api.GetFriends(user_id=friendUser.GetId())

commonFollows = []

for userFollower in userFollows:
    for friendUserFollower in friendUserFollows:
        if userFollower.GetId() == friendUserFollower.GetId():
            commonFollows.append(userFollower)

if len(commonFollows) > 0:
    print ("You both follow %d common people." % len(commonFollowers))

    if raw_input("See common followers names? (y/n) : ") == 'y':
        for commonPerson in commonFollowers:
            print("------ ----- ***** ----- -----")
            print("ScreenName: %s" % commonPerson.GetScreenName())
            print("------ ----- ***** ----- -----")
else:
    print ("You don't follow anyone in common")