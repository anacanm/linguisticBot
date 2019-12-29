#Anacan Mangelsdorf
import tweepy
import emoji as EMOJI
import datetime
import time
import random
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
######################################
api = None
emojiList = []
######################################
def connectToAPI():
    global api
    #setting up credentials from the config file and connecting to API
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



def loadEmojiList():
    global emojiList
    file = open('emojiTxt.txt', 'r')
    write = open("timeSortedTweets.txt", "a")
    read = (file.readline())
    for emoji in read:
        emojiList.append(emoji)




def getText(searchResult):
    try:
        if(hasattr(searchResult, "retweeted_status")): #if its a retweet
            try: #if its extended, get the full extended
                text = searchResult.retweeted_status.full_text
            except AttributeError: #otherwise, just get the normal text
                text = searchResult.retweeted_status.text
        else:
            try: #if its extended, get the full extended
                text = searchResult.full_text
            except AttributeError: #otherwise, just get the normal text
                text = searchResult.text
    except:
        return ""

    return text




def main():
    connectToAPI()
    loadEmojiList()
    global api


    #TODO remove tweetList and all occurences
    tweetList = [] #this is a list that contains ALL TWEETS that are loaded through API


    maxTweets = 1000
    while (len(tweetList)< maxTweets): #TODO change condition to while rowCount<1000
        text = ""
        emojisInText = ""
        textContainsEmoji = False
        #generates a random emoji from emojiList
        randomEmoji = emojiList[random.randint(0,len(emojiList)-1)]
        #finds a tweet using the random emoji
        searchResult = api.search(q=randomEmoji, tweet_mode = "extended", lang = 'en', result_type = 'popular', count = 1)
        
        '''the below block is a check to make sure the api worked correctly'''
        if(len(searchResult)<1): #if there is no tweet found 
            #NOTE might need a time.sleep(5) here
            continue
        

        text = getText(searchResult[0])


        '''the below block is a check to make sure the api worked correctly'''
        if(text == ""): #if the api.search isn't being desirable and returns an empty string as the text
            #NOTE might need a time.sleep(5) here
            continue


        for char in (text): #iterates through the text of each individual tweet's text
            if (char in EMOJI.UNICODE_EMOJI): #this returns true if the character is an emoji
                textContainsEmoji = True #if there was an emoji found in the tweet, then the tweet contains an emoji
                emojisInText += char
        
        '''the below block is a check to make sure the api worked correctly'''
        if(not textContainsEmoji):#if there is no emoji in the text, i.e. api.search messed up
            #NOTE might need a time.sleep(5) here
            continue

        #below is a datetime object that represents when the tweet was created at (posted)
        createdAt = searchResult[0].created_at
        #below is a string that represents when the tweet was created in [MM/DD/YYYY 24HR:Minute] format
        formattedDateTime = createdAt.strftime("%m/%d/%Y") + " " + createdAt.strftime("%H:%M")

        #the below code does sentiment analysis of the text
        sentimentAnalyzer = SentimentIntensityAnalyzer()
        scores = sentimentAnalyzer.polarity_scores(text)
        sentiment = scores["compound"]

        

        numberEmojis = len(emojisInText)

        print(text)
        print()
        print(emojisInText, "are in the text, and there are", numberEmojis, "emojis") 
        print(sentiment, "is the sentiment score")
        print(formattedDateTime)
        print("////////////////////////////////////")
        print("////////////////////////////////////")
        print()
        

        time.sleep(5)

main()
        
