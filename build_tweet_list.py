#!/usr/bin/env python

import twitter
import time

user = 'twitter-user'
all_tweets = []

api = twitter.Api(
    consumer_key        = '',
    consumer_secret     = '',
    access_token_key    = '',
    access_token_secret = ''
)

def list_tweets(user, last_tweet_id):
    t = []
    lastweet = None
    statuses = api.GetUserTimeline(
        user_id = user,
        count = '200',
        max_id = last_tweet_id
    )

    for s in statuses:
        tweetid = str(s.id)
        tweetdate = str(s.created_at)

        if lastweet is tweetid:
            continue
        else:
            lastweet = tweetid
            tinfo = '%s;%s' % (tweetid, tweetdate)
            t.append(tinfo)

    return t

f = open('tweets.lst', 'ws')

while True:
    try:
        this_batch_last_tweet
    except NameError:
        this_batch_last_tweet = None

    try:
        last_batch_last_tweet
    except NameError:
        last_batch_last_tweet = None

    tweets = list_tweets(user, this_batch_last_tweet)
    this_batch_last_tweet = tweets[-1].split(';')[0]

    print 'number of tweets            : %s' % len(all_tweets)
    print 'last batch last tweet ID    : %s' % last_batch_last_tweet
    print 'current batch last tweet ID : %s' % this_batch_last_tweet

    if this_batch_last_tweet != last_batch_last_tweet:
        for t in tweets:
            current_tweet_id = t.split(';')[0]
            try:
                last_tweet_id
            except NameError:
                last_tweet_id = None

            if current_tweet_id == last_tweet_id:
                print '### SKIPPING TWEET ###'
                print "current tweet id  : %s" % str(current_tweet_id)
                print "last tweet id     : %s" % str(last_tweet_id)
                continue
            else:
                all_tweets.append(t)
                f.write(t + '\n')

            last_tweet_id = current_tweet_id
    else:
        break

    last_batch_last_tweet = this_batch_last_tweet

print len(all_tweets)
f.close()
