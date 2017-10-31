#!/usr/bin/env python
"""Script to purge all your Likes/Favorites on Twitter."""
import twitter
import time

user = 'user-id'
api = twitter.Api(
    consumer_key='',
    consumer_secret='',
    access_token_key='',
    access_token_secret=''
)


def get_twitter_favs(user, last_entry):
    """Get Favs/Likes from Twitter API (max 200 entries at a time).

    Get a list of favorites/likes from Twitter. If we have a 'last' entry, we
    us this ID as a starting point and only query favs with a higher id than
    that.
    """
    if last_entry:
        likes = api.GetFavorites(user_id=user,
                                 count='200',
                                 since_id=last_entry)
    else:
        likes = api.GetFavorites(user_id=user, count='200')
    return likes


while True:
    try:
        current_batch_last_entry
    except NameError:
        current_batch_last_entry = None

    try:
        last_batch_last_entry
    except NameError:
        last_batch_last_entry = None

    favs = get_twitter_favs(user, current_batch_last_entry)
    if favs:
        current_batch_last_entry = favs[-1].id
        print 'total favs                : %s' % len(favs)
        print 'previous batch, last entry: %s' % last_batch_last_entry
        print 'current batch, last entry : %s' % current_batch_last_entry

        if current_batch_last_entry != last_batch_last_entry:
            for f in favs:
                print "Deleting Like with ID %s" % (f.id)

                try:
                    api.DestroyFavorite(f)
                    time.sleep(15)
                except twitter.TwitterError:
                    print "ERR: Fav with ID %s could not be deleted" % (f.id)
        else:
            break

        last_batch_last_entry = current_batch_last_entry
    else:
        print "Could not retrieve favourites from Twitter."
        break
