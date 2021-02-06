#!/usr/bin/env python

import twitter
import datetime
import time

user = 'twitterhandle'
now = datetime.datetime.utcnow()
cutoff_date = datetime.datetime(year=2020, day=1, month=1)

deleted_tweets = []
this_batch_last_tweet = None
last_batch_last_tweet = None
last_tweet_id = None

api = twitter.Api(sleep_on_rate_limit=True,
                  consumer_key='',
                  consumer_secret='foo',
                  access_token_key='foo',
                  access_token_secret='foo')


def get_tweets(user, last_tweet_id):
    tweets = []
    lastweet = None
    statuses = api.GetUserTimeline(user_id=user, count='200',
                                   max_id=last_tweet_id,
                                   include_rts=True)

    for s in statuses:
        tweetid = str(s.id)
        tweetdate = str(s.created_at)

        if lastweet is tweetid:
            continue
        else:
            lastweet = tweetid
            tinfo = "{};{}".format(tweetid, tweetdate)
            tweets.append(tinfo)

    return tweets


print("Time now: {}".format(now))
print("Cutoff date : {}".format(cutoff_date))
f = open('tweets.lst', 'w')

while True:
    tweets = get_tweets(user, this_batch_last_tweet)
    this_batch_last_tweet = tweets[-1].split(';')[0]

    print('number of tweets            : {}'.format(len(tweets)))
    print('last batch last tweet ID    : {}'.format(last_batch_last_tweet))
    print('current batch last tweet ID : {}'.format(this_batch_last_tweet))

    if this_batch_last_tweet != last_batch_last_tweet:
        for t in tweets:
            current_tweet_id = t.split(';')[0]
            if current_tweet_id == last_tweet_id:
                print("### SKIPPING TWEET ###")
                print("current tweet id  : {}".format(current_tweet_id))
                print("last tweet id     : {}".format(str(last_tweet_id)))
                continue
            else:
                tweetid = str(t.id)
                tweetdate = str(t.created_at)
                status_tstamp_weekday = tweetdate.split(' ')[0]
                status_tstamp_month = tweetdate.split(' ')[1]
                status_tstamp_day = tweetdate.split(' ')[2]
                status_tstamp_hour = tweetdate.split(' ')[3].split(":")[0]
                status_tstamp_minute = tweetdate.split(' ')[3].split(":")[1]
                status_tstamp_second = tweetdate.split(' ')[3].split(":")[2]
                status_tstamp_year = tweetdate.split(' ')[5]
                status_tstamp_strptime = '{} {} {} {}:{}:{} {}'.format(
                    status_tstamp_weekday,
                    status_tstamp_month,
                    status_tstamp_day,
                    status_tstamp_hour,
                    status_tstamp_minute,
                    status_tstamp_second,
                    status_tstamp_year)
                status_tstamp = datetime.datetime.strptime(
                    status_tstamp_strptime,
                    '%a %b %d %H:%M:%S %Y')

                if status_tstamp <= cutoff_date:
                    print("Deleting tweet {} {}".format(tweetid, tweetdate))
                try:
                    api.DestroyStatus(tweetid)
                    deleted_tweets.append(t)
                    f.write(t + '\n')
                    time.sleep(15)
                except twitter.TwitterError:
                    print("ERR: Tweet with ID {}"
                          " could not be deleted".format(tweetid))
                else:
                    print("Skipping tweet {}".format(tweetid))
                    print("Tweet date {} earlier than cutoff date {}".format(
                            tweetdate,
                            cutoff_date))
            last_tweet_id = current_tweet_id
    else:
        break

    last_batch_last_tweet = this_batch_last_tweet

print("Deleted tweets: {}".format(len(deleted_tweets)))
f.close()
