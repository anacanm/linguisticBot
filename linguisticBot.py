#Anacan Mangelsdorf

import tweepy
import emoji
import datetime
import matplotlib.pyplot as plot

# @Article{Hunter:2007,
#   Author    = {Hunter, J. D.},
#   Title     = {Matplotlib: A 2D graphics environment},
#   Journal   = {Computing in Science \& Engineering},
#   Volume    = {9},
#   Number    = {3},
#   Pages     = {90--95},
#   abstract  = {Matplotlib is a 2D graphics package used for Python for
#   application development, interactive scripting, and publication-quality
#   image generation across user interfaces and operating systems.},
#   publisher = {IEEE COMPUTER SOC},
#   doi       = {10.1109/MCSE.2007.55},
#   year      = 2007
# }

# Authenticate to Twitter APIs, dont worry about how this operates
auth = tweepy.OAuthHandler("Mj8AXEjEUKhAvJXSRg8KrEuU0", "W2jmFmW2Zfqulw9si7pF6pnt6eCs2WAWXKHXTXS9etudPtdFGg") #consumer API key, consumer API secret key
auth.set_access_token("1192250121926262784-TldMVjsGLIoal7rmk08pS0zglDgvF4", "pTxr8mvLJeLjwzNMqA9WGXg6d52PJPWfrRxJvPUCKTRFD")#access token, access secret token

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
#api.update_status('Test tweet from Tweepy:)')

'''###################################################'''

def fillEmojiIndexDict():
    #makes a dictionary to be updated, where each key is an index and its corresponding value is how many times an emoji was found at that index
    #this dictionary will not remove elements where the value is 0
    #there are 280 possible characters in a tweet, so the indeces will go from 0-279
    dict = {}
    count = 0
    while(count<280):
        dict[count] = 0
        count+=1
    return dict

def fillEmojiCountDict():
    #makes a dictionary to be updated, where each key is an emoji, and its corresponding value is how many times the emoji occurs
    #this dictionary will not remove elements where the value is 0
    #there are currently 2811 emojis as of 11/12/19
    dict = {}
    for key in (emoji.UNICODE_EMOJI):
        dict[key] = 0
    return dict   

def fillEmojiHourDict():
    dict = {}
    count = 0
    while(count<24):
        dict[count]=0
        count+=1
    return dict
    

def trimDict(dict):#takes a dictionary as a parameter, and returns a new dictionary that only contains keys from the original dict who's values are >0
    trimmedDict = {}
    for key in dict:
        if(dict[key]>0):
            trimmedDict[key]=dict[key]
    return trimmedDict 
    
#emojiFile = open("emojis.txt", "r") #this is a file containing all of the emojis, not encoded
tweetList = [] #this is a list that contains ALL TWEETS that are loaded through API
containEmojiTweets = [] #this is a list that will only contain tweets that contain emojis
emojiTweetsCreatedAt = [] #this is a list that will contain the date and time of when tweets that contain emojis are created, data types are datetime
timeline = api.home_timeline() #this loads my whole twitter timeline
emojiIndexDict = fillEmojiIndexDict()
emojiCountDict = fillEmojiCountDict()
emojiHourDict = fillEmojiHourDict()



#TODO rather than reading from the timeline, read from random? tweets (this is for later because I can control timeline)
#TODO make a list that only has tweets with emojis in them, after this I should incorporate data analysis

#TODO data analyses
#record where (what indeces) emojis are located at, probably using a dictionary where the keys are indexes (280 characters max in a tweet), and the values are the number of times an emoji occurs at that index
#how many times each emoji is used, again a dictionary probably, where every emoji is a key, and the values are the number of times that emoji occurs
#when emojis are used in general, plot it on a graph
#when each emoji is used




for count, tweet in enumerate(timeline): #this adds every tweet in the timeline to a list
    tweetList.append(tweet)


# for count,line in enumerate(emojiFile): #this adds every emoji from the file as a specific element to the emojiList
#     emojiList = line.split()
#TODO rather than iterating through a list of tweet's text, iterate through the tweets themselves and just access the text when needed
#the, add the entire tweet to a list so its other properties can be accessed if needed

for tweetIndex,tweet in enumerate(tweetList): #iterates through list of tweet
    for charIndex, char in enumerate(tweet.text): #iterates through the text of each individual tweet's text
        if (char in emoji.UNICODE_EMOJI): #this returns true if the character is an emoji
            tweetContainsEmoji = True #if there was an emoji found in the tweet, then the tweet contains an emoji
            emojiIndexDict[charIndex]+=1  #this updates the emojiIndexDict dictionary, where each key is an index and the value is the number of times that an emoji occurs at that index
            emojiCountDict[char]+=1
            #print(char, "is an emoji! It is at index", charIndex) 
    if(tweetContainsEmoji): #if the tweet contains an emoji, then it is added to the list that 
        containEmojiTweets.append(tweet) 
        tweetContainsEmoji = False

trimmedEmojiIndexDict = trimDict(emojiIndexDict)
trimmedEmojiCountDict = trimDict(emojiCountDict)
sortedTrimmedEmojiCountList = sorted(trimmedEmojiCountDict.items(), key=lambda kv: kv[1], reverse=True)
#sortedTrimmedEmojiCountList is a sorted list of tuples(len = 2) where the first element is an emoji, and the second element is the # of occurences
#of that emoji, this list is sorted in descending order

for tweet in containEmojiTweets: #emojiTweetsCreatedAt is a list that now contains the datetime objects for when every emoji-containing-tweet was tweeted/created
    emojiTweetsCreatedAt.append(tweet.created_at)




#the code below works with matplotlib to make a graph of the hourly usage of tweets
for time in emojiTweetsCreatedAt:
    emojiHourDict[int(time.strftime("%H"))]+=1

trimmedEmojiHourDict = trimDict(emojiHourDict)

xAxis = []
yAxis = []
for key in trimmedEmojiHourDict:
    xAxis.append(key)
    yAxis.append(trimmedEmojiHourDict[key])


plot.bar(xAxis,yAxis)
plot.xlabel("Time during a day(24hr)")
plot.ylabel("Number Of Tweets That Emojis Are Used In")
plot.title("Emoji Usage Throughout the Day")
plot.show()





