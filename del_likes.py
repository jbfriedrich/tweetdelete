#!/usr/bin/env python

import twitter
import time

api = twitter.Api(
    consumer_key        = '',
    consumer_secret     = '',
    access_token_key    = '',
    access_token_secret = ''
)

user    = 'twitterhandle'
likes   = api.GetFavorites(user_id = user, count = '200')

for like in likes:
    print "Deleting Like with ID %s" % (like.id)

    try:
        api.DestroyFavorite(like)
        time.sleep(15)
    except twitter.TwitterError:
        print "ERR: Like with ID %s could not be deleted" % (like.id)
