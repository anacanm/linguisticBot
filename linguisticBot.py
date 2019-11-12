#Anacan Mangelsdorf

import tweepy
import emoji
# Authenticate to Twitter APIs, dont worry about how this operates
auth = tweepy.OAuthHandler("Mj8AXEjEUKhAvJXSRg8KrEuU0", "W2jmFmW2Zfqulw9si7pF6pnt6eCs2WAWXKHXTXS9etudPtdFGg") #consumer API key, consumer API secret key
auth.set_access_token("1192250121926262784-TldMVjsGLIoal7rmk08pS0zglDgvF4", "pTxr8mvLJeLjwzNMqA9WGXg6d52PJPWfrRxJvPUCKTRFD")#access token, access secret token

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
#api.update_status('Test tweet from Tweepy:)')

'''###################################################'''

def fillEmojiIndexDict():
    dict = {}
    #makes a dictionary to be updated, where each key is an index and its corresponding value is how many times an emoji was found at that index
    #this dictionary will not remove elements where the value is 0
    #there are 280 possible characters in a tweet, so the indeces will go from 0-279
    count = 0
    while(count<280):
        dict[count] = 0
        count+=1
    return dict
def trimIndexDict(dict):#takes emojiIndexDict dictionary as a parameter, and returns a new dictionary that only contains keys who's values is >0
    trimmedDict = {}
    count = 0
    while(count<len(dict)):
        if(dict[count]>0):
            trimmedDict[count]=dict[count]
        count+=1
    return trimmedDict




    
    
#emojiFile = open("emojis.txt", "r") #this is a file containing all of the emojis, not encoded
tweetList = [] #this is a list that contains all tweets that are loaded through API
#emojiList = [] #this is a list that contains all of the emojis, each as their own element, from the emojis.txt file, might not need
timeline = api.home_timeline() #this loads my whole twitter timeline
emojiIndexDict = fillEmojiIndexDict()


#TODO rather than reading from the timeline, read from random? tweets (this is for later because I can control timeline)
#TODO make a list that only has tweets with emojis in them, after this I should incorporate data analysis

#TODO data analyses
#record where (what indeces) emojis are located at, probably using a dictionary where the keys are indexes (280 characters max in a tweet), and the values are the number of times an emoji occurs at that index
#how many times each emoji is used, again a dictionary probably, where every emoji is a key, and the values are the number of times that emoji occurs




for count, tweet in enumerate(timeline): #this adds the text of every tweet to a list
    tweetList.append(tweet.text)


# for count,line in enumerate(emojiFile): #this adds every emoji from the file as a specific element to the emojiList
#     emojiList = line.split()
    
for tweetIndex,tweet in enumerate(tweetList): #iterates through list of tweet's text
    for charIndex, char in enumerate(tweet): #iterates through the text of each individual tetx
        if (char in emoji.UNICODE_EMOJI): #this returns true if the character is an emoji
            emojiIndexDict[charIndex]+=1  #this updates the emojiIndexDict dictionary, where each key is an index and the value is the number of times that an emoji occurs at that index
            #print(char, "is an emoji! It is at index", charIndex) 

trimmedEmojiIndexDict = trimIndexDict(emojiIndexDict)
#trimmedEmojiIndexDict now contains all keys of emojiIndexDict who's values are >0 
#trimmedEmojiIndexDict only contains indexes where emojis did occur, and the values are the number of occurences
                                                    

