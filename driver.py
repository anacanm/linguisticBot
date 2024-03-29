#!/usr/bin/env python3

#Made by Anacan Mangelsdorf
#https://github.com/anacanm
#https://www.linkedin.com/in/anacan-mangelsdorf-6babb1194/

import tweepy
import os
import sqlite3
from sqlite3 import Error
import json
import emoji as EMOJI
from datetime import datetime
import random
import csv
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
######################################
api = None

tableTitle = ("[" + (datetime.today().strftime("%m/%d/%Y")) + " " + datetime.now().strftime("%H:%M") + "]").replace("/","_").replace(":", "_")

conn = None
cursor = None
rowCount = 0

emojiList = []

tweetsToGather = 1000
#NOTE tweetsToGather is the number of tweets that is desired to be added to the table
######################################
def setupDB():#this connects to the database and creates a new table
    global conn
    global cursor

    filePath = os.path.join(os.getcwd(), "tweets.db")
    
    #the below code connects to the database or prints an error
    try:
        conn = sqlite3.connect(filePath)
    except Error as e:
        print(e)

    #the below code creates a new table

    createStatement = """ CREATE TABLE IF NOT EXISTS {} (
    tweetText text PRIMARY KEY,
    emojisContained text NOT NULL,
    numberEmojis integer NOT NULL,
    sentiment decimal NOT NULL,
    dateTime text NOT NULL
    ); """.format(tableTitle)
    
    try:
        cursor = conn.cursor()
        cursor.execute(createStatement)
    except Error as e:
        print(e)
        


def insertData(tweetText, emojisContained, numberEmojis, sentiment, dateTime):
    global conn
    global cursor
    global rowCount
    
    # insertStatement = """ INSERT INTO {} (tweetText, emojisContained, numberEmojis, sentiment, dateTime)
    # VALUES("{}", "{}", {}, {}, "{}")""".format(tableTitle,tweetText, emojisContained, numberEmojis, sentiment, dateTime)
    
    #the below statement inserts data into the table, as long as there are no text duplicates
    insertStatement = """ INSERT INTO {} (tweetText, emojisContained, numberEmojis, sentiment, dateTime)
    SELECT *
    FROM (VALUES("{}", "{}", {}, {}, "{}"))
    WHERE "{}" NOT IN (SELECT tweetText FROM {})""".format(tableTitle, tweetText, emojisContained, numberEmojis, sentiment, dateTime, tweetText, tableTitle)

    rowStatement = """ SELECT COUNT(*) FROM {}""".format(tableTitle)


    try:
        cursor.execute(insertStatement)
        conn.commit() 
        cursor.execute(rowStatement)
        rowCount = (cursor.fetchall())[0][0]
    except Error as e:
        print(e)
        print(insertStatement)
    #NOTE if running into errors with inserting data, the issue may lie in when the commit/close is called

######################################
'''here is the end of the database methods'''
'''below is the twitter and text methods'''

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

    return (text.replace("\"", "\'"))



def writeToCSV():
    getStatement =  """SELECT *
    FROM {}""".format(tableTitle)
    fileName = (tableTitle.replace("[", "").replace("]", "")) + ".csv"

    try:
        cursor.execute(getStatement)
        data = cursor.fetchall()

        with open(os.path.join(os.getcwd(),fileName), "w+") as csvFile:
            header = ["tweetText","emojisContained", "numberEmojis", "sentiment", "dateTime"] 
            writer = csv.DictWriter(csvFile, fieldnames = header)
            writer.writeheader()

            for row in data:
                writer.writerow({header[0]: row[0], header[1]: row[1], header[2]: row[2], header[3]: row[3], header[4]: row[4]})

    except Error as e:
        print(e)



def main():
    setupDB()
    connectToAPI()

    loadEmojiList()
    global api

    while(rowCount<tweetsToGather):
        #print(rowCount, "rows")
        time.sleep(5)
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

        insertData(text,emojisInText, numberEmojis, sentiment, formattedDateTime)

        
    writeToCSV()
    cursor.close()

main()
print("Done! A new csv file is now in your current directory!")
