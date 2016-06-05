#!/usr/bin/env python

import twitter
import time

api = twitter.Api(
    consumer_key        = '',
    consumer_secret     = '',
    access_token_key    = '',
    access_token_secret = ''
)

print "Deleting old tweets..."

counter=0
tweets = 0
f = open('tweets.lst', 'r')

for tweet in f:
    tweetid = tweet.split(';')[0]
    tweetdate = tweet.split(';')[1].rstrip('\n')
    print "Deleting tweet %s from %s" % (tweetid, tweetdate)
    try:
        api.DestroyStatus(tweetid)
    except twitter.TwitterError:
        print "Tweet with ID %s could not be deleted" % (tweetid)
    tweets += 1
    counter +=1

    if counter == 15:
        time.sleep(900)
        counter = 1

f.close()
print "Deleted a total of %s tweets" % tweets
