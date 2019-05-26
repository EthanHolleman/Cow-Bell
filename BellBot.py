#!/usr/bin/python
import praw, random
def post():
    reddit = praw.Reddit(client_id='su_QWDMHVla0Fw',
                         client_secret='secret',
                         username='TheCowBellBot',
                         password='key',
                         user_agent='cowbell')

    with open("Listings.txt") as lists:
        headList = []
        for line in lists:
            headList.append(line)

    for i in range(1,4):
        rand = random.randint(0,len(headList))
        listing = headList[rand].split(",")
        title = "ID: {} | Owner: {} | Location: {}".format(listing[0],listing[1],listing[4])
        #title = "ID: " + listing[0] + " | "+ " Owner: " + listing[1] + " Location: " + listing[4]
        post = listing[5] + "\n\nContact Info\n\n" + "Email: " +listing[2] + "\n\n" + "Phone " + listing[3]

        print("Now posting {}".format(title))

        reddit.subreddit('CattleExchange').submit(title = title, selftext = post)
