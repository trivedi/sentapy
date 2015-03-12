#!/usr/bin/python/
from __future__ import print_function

import credentials
import tweepy, time
import NaiveBayes

ACCESS_KEY = credentials.ACCESS_KEY
ACCESS_SECRET = credentials.ACCESS_SECRET
CONSUMER_KEY = credentials.CONSUMER_KEY
CONSUMER_SECRET = credentials.CONSUMER_SECRET
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
