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
    printUserDetails(friendUser)
else:
    print ("User '%s' not found." %friendScreenName)

print ("Looking for people you both follow..")
userFollows = api.GetFriendIDs(user_id=user.GetId(), screen_name=user.GetScreenName())
print("%s follows %d people." %(user.GetScreenName(), len(userFollows)))

friendUserFollows = api.GetFriendIDs(user_id=friendUser.GetId(), screen_name=friendUser.GetScreenName())
print("%s follows %d people." %(friendUser.GetScreenName(), len(friendUserFollows)))

commonFollows = [followerId for followerId in userFollows if followerId in friendUserFollows]

if len(commonFollows) > 0:
    print ("You both follow %d common people." % len(commonFollows))

    if raw_input("See common followers names? (y/n) : ") == 'y':
        for commonPersonId in commonFollows:
            print("------ ----- ***** ----- -----")
            print("ScreenName: %s" % api.GetUser(user_id=commonPersonId).GetScreenName())
            print("------ ----- ***** ----- -----")
else:
    print ("You don't follow anyone in common")

print ("Looking for common followers..")
userFollowers = api.GetFollowers(user_id=user.GetId(), screen_name=user.GetScreenName())
friendUserFollowers = api.GetFollowers(user_id=friendUser.GetId(), screen_name=friendUser.GetScreenName())

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
