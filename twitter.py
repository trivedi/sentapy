#!/usr/bin/python/
from __future__ import print_function

import tweepy, time
import NaiveBayes

ACCESS_KEY = '361596509-0182QQDamwiRcPHYWICdsg7mIMWxS1h8sP2Umkcb'
ACCESS_SECRET = 'eVatVboU1WowO4odY3nahOXpLYrbvB4Hr4pKSzVqlX2oC'
CONSUMER_KEY = 'hQwtjtpcj4mWRLvPtJ88g'
CONSUMER_SECRET = 'Kq5C2EvtyhKHrnzVo1OW63LGIvPzSkRjsEEGb3mIbig'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

tweets = {}

def login():
	user = api.me()
	print ("> Successfully logged into Twitter!")

def tracker(track):
	print('> Script will start tracking "' + track + '". Tweets should start to appear below.')
	print

def stream(track):
	sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
	sapi.filter(track=[track])


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
		tweet = status.text
		if tweet in tweets: # avoid analyzing duplicate tweets (duplicates occur a lot because of retweeting)
			tweets[tweet] += 1
		else:
			tweets[tweet] = 1
			print(tweet, end=" => ")
			NaiveBayes.c.classify(tweet)
			time.sleep(2)


def run():
    login()
    track = raw_input('> Enter @username, #hashtag, or word to query: ')
    tracker(track)
    stream(track)

if __name__ == '__main__':
    run()
