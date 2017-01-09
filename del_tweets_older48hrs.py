#!/usr/bin/env python

import twitter
import datetime
import time

api = twitter.Api(
    consumer_key        = '',
    consumer_secret     = '',
    access_token_key    = '',
    access_token_secret = ''
)

user        = 'twitterhandle'
now         = datetime.datetime.utcnow()
cutoff_date = now - datetime.timedelta(hours=48)
statuses    = api.GetUserTimeline(user_id = user, count = '200')
skip_tweets = str(["123456789012345678", "123456789012345678"])

print "Time now    : %s" % (now)
print "Cutoff date : %s" % (cutoff_date)

for s in statuses:
    tweetid     = str(s.id)
    tweetdate   = str(s.created_at)

    if tweetid in skip_tweets:
        print 'Skipping tweet %s as specified' % (tweetid)
        continue
    else:
        status_tstamp_weekday   =   tweetdate.split(' ')[0]
        status_tstamp_month     =   tweetdate.split(' ')[1]
        status_tstamp_day       =   tweetdate.split(' ')[2]
        status_tstamp_hour      =   tweetdate.split(' ')[3].split(":")[0]
        status_tstamp_minute    =   tweetdate.split(' ')[3].split(":")[1]
        status_tstamp_second    =   tweetdate.split(' ')[3].split(":")[2]
        status_tstamp_year      =   tweetdate.split(' ')[5]

        status_tstamp_strptime = '%s %s %s %s:%s:%s %s' % (
            status_tstamp_weekday,
            status_tstamp_month,
            status_tstamp_day,
            status_tstamp_hour,
            status_tstamp_minute,
            status_tstamp_second,
            status_tstamp_year
        )

        status_tstamp = datetime.datetime.strptime(
            status_tstamp_strptime,
            '%a %b %d %H:%M:%S %Y'
        )

        if status_tstamp <= cutoff_date:
            print "Deleting tweet %s (%s)" % (tweetid, tweetdate)
            try:
                api.DestroyStatus(tweetid)
                time.sleep(15)
            except twitter.TwitterError:
                print "ERR: Tweet with ID %s could not be deleted" % (tweetid)

        else:
            print "Skipping tweet %s" % (tweetid)
            print "Tweet date %s earlier than cutoff date %s" %(
                tweetdate,
                cutoff_date
            )
