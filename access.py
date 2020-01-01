#!/usr/bin/env python3

#Made by Anacan Mangelsdorf
#https://github.com/anacanm
#https://www.linkedin.com/in/anacan-mangelsdorf-6babb1194/

import sqlite3
from sqlite3 import Error
import csv
import os
tableTitle = ""
fileName = ""
conn = None
cursor = None

def setupDB():
    global conn
    global cursor

    filePath = os.path.join(os.getcwd(), "tweets.db")

    try:
        conn = sqlite3.connect(filePath)
        cursor = conn.cursor()
    except Error as e:
        print(e)

def printTableNames():
    tableNameStatement = """SELECT name
    FROM sqlite_master
    WHERE type = "table" """

    cursor.execute(tableNameStatement)

    data = cursor.fetchall()
    for table in data:
        print(table[0])






def writeToCSV():
    getStatement =  """SELECT *
    FROM {}""".format(tableTitle)
    
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
    global tableTitle
    global fileName
    print("Please type the title of the table that you would like to access")
    print("The available tables are:")
    printTableNames()
    print("Table format should follow \"MM_DD_YYYY HR_MN\",hours are in 24hr format")
    print("I didn't put user validation here, so please type it correctly(don't include quotes).")
    inp = input()
    tableTitle = "[" + inp + "]"

    fileName = inp + ".csv"

    writeToCSV()
    cursor.close()
    print("The new csv file titled {} is now in your current directory!".format(fileName))

main()
