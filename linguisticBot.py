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

#emojiFile = open("emojis.txt", "r") #this is a file containing all of the emojis, not encoded
tweetList = [] #this is a list that contains all tweets that are loaded through API
#emojiList = [] #this is a list that contains all of the emojis, each as their own element, from the emojis.txt file, might not need
timeline = api.home_timeline() #this loads my whole twitter timeline


#TODO rather than reading from the timeline, read from random? tweets (this is for later because I can control timeline)
#TODO make a list that only has tweets with emojis in them, after this I should incorporate data analysis

#TODO data analyses
#record where (what indeces) emojis are located at, probably using a dictionary where the keys are indexes (280 characters max in a tweet), and the values are the number of times an emoji occurs at that index
#how many times each emoji is used, again a dictionary probably, where every emoji is a key, and the values are the number of times that emoji occurs


for count, tweet in enumerate(timeline): #this adds the text of every tweet to a list
    tweetList.append(tweet.text)


# for count,line in enumerate(emojiFile): #this adds every emoji from the file as a specific element to the emojiList
#     emojiList = line.split()
    
i = j = 0
for tweet in tweetList:
    for index,char in enumerate(tweet):
        if (char in emoji.UNICODE_EMOJI): #this returns true if the character is an emoji
            print(char, "is an emoji! It is at index", index) 