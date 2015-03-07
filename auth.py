import twitter
import fileinput
import constants
import urllib2
import lxml.html
import operator
from collections import Counter

token_file=fileinput.input("my_keys.txt")
firstUserTimeline = []
friendUserTimeline = []

def get_user_timeline(user):
    url = '%s/statuses/user_timeline.json?count=3200&trim_user=0&exclude_replies=0&include_rts=1&screen_name=%s' % \
          (api.base_url,user.GetScreenName())

    json = api._RequestUrl(url, 'GET')
    data = api._ParseAndCheckTwitter(json.content)

    return data


def evaluate_common_ppl_followed(user, friendUser):
    print ("Looking for people you both follow..")
    user_follows = api.GetFriendIDs(user_id=user.GetId(), screen_name=user.GetScreenName())
    #print("%s follows %d people." % (user.GetScreenName(), len(user_follows)))

    friend_user_follows = api.GetFriendIDs(user_id=friendUser.GetId(), screen_name=friendUser.GetScreenName())
    #print("%s follows %d people." %(friendUser.GetScreenName(), len(friend_user_follows)))

    common_follows = [followerId for followerId in user_follows if followerId in friend_user_follows]

    if len(common_follows) > 0:
        print ("You both follow %d common people." % len(common_follows))

        if raw_input("See common followers names? (y/n) : ") == 'y':
            for commonPersonId in common_follows:
                print("------ ----- ***** ----- -----")
                print("ScreenName: %s" % api.GetUser(user_id=commonPersonId).GetScreenName())
    else:
        print ("You don't follow anyone in common")


def evaluate_common_followers(user, friendUser):
    print ("Looking for common followers..")
    user_followers = api.GetFollowerIDs(user_id=user.GetId(), screen_name=user.GetScreenName())
    friend_user_followers = api.GetFollowerIDs(user_id=friendUser.GetId(), screen_name=friendUser.GetScreenName())

    #print ("%s is followed by %d people" %(user.GetScreenName(),len(user_followers)))
    #print ("%s is followed by %d people" %(friendUser.GetScreenName(),len(friend_user_followers)))

    common_followers = [followerId for followerId in user_followers if followerId in friend_user_followers]

    if len(common_followers) > 0:
        print ("You both have %d common followers." % len(common_followers))

        if raw_input("See common followers names? (y/n) : ") == 'y':
            for commonPerson in common_followers:
                print("------ ----- ***** ----- -----")
                print("ScreenName: %s" % api.GetUser(user_id=commonPerson).GetScreenName())
    else:
        print ("You don't have common followers..")


def get_user_mentions(userTimeline, user):
    if not userTimeline:
        return
    source_tweeter = userTimeline[0]['user']['screen_name']
    for tweet in userTimeline:
        user_mentions = tweet['entities']['user_mentions']
        for userMention in user_mentions:
            if userMention['id'] == user.GetId():
                tweets_with_friend_mention.append(tweet)

    print ("%s's tweets with %s mention: %d" %(source_tweeter, user.GetScreenName(), len(tweets_with_friend_mention)))

def process_user_timeline(userTimeLine):
    tweets_with_friend_mention = []
    user_tweet_sources = dict()
    user_tweet_mention_counters = dict()

    for tweet in userTimeLine:
        """
        Get the user mention data first
        """
        user_mentions = tweet['entities']['user_mentions']
        if user_mentions:
            for userMention in user_mentions:
                """"""
                user_tweet_mention_counters[userMention['screen_name']]=\
                    user_tweet_mention_counters.get(userMention['screen_name'], 0) + 1

        """
        Get the tweet source next
        """
        tweet_source = lxml.html.fromstring(tweet['source']).text_content()
        user_tweet_sources[tweet_source]=user_tweet_sources.get(tweet_source , 0) + 1

    #print("Here's the user tweet source and counters: ")
    #print user_tweet_sources

    #print ("In the last 3200 tweets, number of tweets with %s's mention %d" %(user.GetScreenName(),
    #                                                                         len(tweets_with_friend_mention)))
    """print ("Tweets:")
    print ("\t----- ----- ***** ----- -----")
    for tweet in tweets_with_friend_mention:
        print ("\t%s" % tweet['text'])
    print ("\t----- ----- ***** ----- -----")"""

    return tweets_with_friend_mention, sorted(user_tweet_sources.items(), key=operator.itemgetter(1), reverse=True)\
        , sorted(user_tweet_mention_counters.items(), key=operator.itemgetter(1), reverse=True)


def print_top_mentions(user_tweet_mention_counter, userName, n=5):
    if not user_tweet_mention_counter:
        return

    print("\n***** ***** ***** ***** *****")

    print ("Lets see the top %d users %s has mentioned recently.." %(n,userName))
    i=0
    for (k, v) in user_tweet_mention_counter:
        if i < n:
            print ("%s : %d" %(k,v))
            i+=1


def print_user_tweet_sources(user_tweet_sources, userName):

    if not user_tweet_sources:
        return

    print("\n***** ***** ***** ***** *****")
    print ("Lets see what are the sources of %s tweets.." %userName)

    for (k, v) in user_tweet_sources:
        print("%s : %d" %(k, v))


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

firstUser = 'ankurdh'

print ("Identifying user '%s'" % firstUser)
user = api.GetUser(screen_name=firstUser)

"""if user:
    print_user_details(user)
else:
    print ("%s not found." % firstUser)
    exit()

if friendUser:
    print_user_details(friendUser)
else:
    print ("%s not found." % friendUser)
    exit()"""

firstUserTimeline = get_user_timeline(user)

tweets_with_friend_mention,user_tweet_sources,user_tweet_mention_counters = process_user_timeline(firstUserTimeline)
print_top_mentions(user_tweet_mention_counters, user.GetScreenName())
print_user_tweet_sources(user_tweet_sources, user.GetScreenName())

friendScreenName = raw_input("\n\nWant to do some stats with a friend? Enter friends screen name: ")
print ("Identifying user '%s'" % friendScreenName)
friendUser = api.GetUser(screen_name=friendScreenName)


friendUserTimeline = get_user_timeline(friendUser)
friends_tweets_with_friend_mention,friends_user_tweet_sources,friends_user_tweet_mention_counters = process_user_timeline(friendUserTimeline)
print_top_mentions(friends_user_tweet_mention_counters, friendUser.GetScreenName())
print_user_tweet_sources(friends_user_tweet_sources, friendUser.GetScreenName())

print("\n***** ***** ***** MUTUAL MENTIONS ***** ***** *****")
get_user_mentions(firstUserTimeline, friendUser)
get_user_mentions(friendUserTimeline, user)

print("\n***** ***** ***** ***** *****")
evaluate_common_ppl_followed(user, friendUser)

print("\n***** ***** ***** ***** *****")
evaluate_common_followers(user, friendUser)