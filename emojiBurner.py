#Anacan Mangelsdorf
import tweepy
import emoji
import datetime
import time
import random
import json


#setting up credentials from the config file
with open('config.json') as configFile:
    data = json.load(configFile)

consumerAPIKey = data["consumerAPIKey"]
consumerAPISecretKey = data["consumerAPISecretKey"]
accessToken = data["accessToken"]
secretAccessToken = data["secretAccessToken"]

# Authenticate to Twitter APIs using credentials from config file
auth = tweepy.OAuthHandler(consumerAPIKey, consumerAPISecretKey) #consumer API key, consumer API secret key
auth.set_access_token(accessToken, secretAccessToken)#access token, access secret token

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

'''###################################################'''



file = open('emojiTxt.txt', 'r')
write = open("timeSortedTweets.txt", "a")
read = (file.readline())
emojiList = []
for emoji in read:
    emojiList.append(emoji)


tweetList = [] #this is a list that contains ALL TWEETS that are loaded through API



maxTweets = 1000
while (len(tweetList)< maxTweets):
    randomEmoji = emojiList[random.randint(0,len(emojiList)-1)]
    searchResult = api.search(q=randomEmoji, tweet_mode = "extended", lang = 'en', result_type = 'popular', count = 1)
    #print(searchResult)
    try:
        if(searchResult[0] not in tweetList):
            if( hasattr(searchResult[0], "retweeted_status")): #if its a retweet
                try: #if its extended, print the full extended
                    print(searchResult[0].retweeted_status.full_text)
                except AttributeError: #otherwise, just print the normal text
                    print(searchResult[0].retweeted_status.text)
            else:
                try:
                    print(searchResult[0].full_text)
                except AttributeError:
                    print(searchResult[0].text)
            #TODO, need the full/extended text
            print("//////////////////////////////////////")
            time.sleep(5)
    except:
        pass

#timeSortedTweetList = sorted(tweetList, key = lambda tweet: tweet.created_at)







        
