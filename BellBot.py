#!/usr/bin/python
from scrape import *
import praw
import random


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

    rand = random.randint(0, len(headList)-1)
    listing = tuple(headList[rand].split(","))
    ID, owner, email, phone, location, description, link = listing
    image_path = get_listing_image(link)

    title = "ID: {} | Owner: {} | Location: {}".format(ID, owner, location)
    post = description + "\n\nContact Info\n\n" + "Email: " + email + "\n\nPhone: "
    + phone + '\n\n[Link to listing]' + '(' + link + ')'

    print("Now posting {}".format(title))

    reddit.subreddit('CattleExchange').submit(title=title, selftext=post)
