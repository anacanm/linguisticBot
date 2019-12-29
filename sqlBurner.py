import os
import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import date
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



tableTitle = "[" + (date.today().strftime("%m/%d/%Y")) + " " + datetime.now().strftime("%H:%M") + "]" 
    #above will be the title of the table: the date in m/d/y with the time in 24 hr format

conn = None #conn is short for connection, that is: connection to the database
cursor = None
rowCount = 0

# def createConnection():
#     #create a database connection to a SQLite database
#     global conn
#     filePath = os.path.join(os.getcwd(), "linguistDB.db") #TODO change database name to tweets.db


#     try:
#         conn = sqlite3.connect(filePath)
#         return conn
#         print("all good baby, you got a big brain")
#     except Error as e:
#         print(e)
#         return None


# def createTable(conn, createStatement): #conn is the connection object, and createStatement is the SQL statement 
#     try:
#         c = conn.cursor()
#         c.execute(createStatement)
#     except Error as e:
#         print(e)


def setup():#this connects to the database and creates a new table
    global conn
    global cursor
    filePath = os.path.join(os.getcwd(), "linguistDB.db") #TODO change database name to tweets.db
    
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


    cursor.execute(insertStatement)
    conn.commit() 
    rowCount = cursor.rowcount
    #NOTE if running into errors with inserting data, the issue may lie in when the commit/close is called






if __name__ == "__main__":    
    setup()



    now = date.today().strftime("%m/%d/%Y") + " " + datetime.now().strftime("%H:%M")


    insertData("foo", "ye", 2, 1.0, now)
    insertData("bar", "ye", 2, 2.0, now)
    insertData("bash", "ye", 2, 3.0, now)
    insertData("foo", "ye", 2, 4.0, now)
    
    cursor.close()
    
