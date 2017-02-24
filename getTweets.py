# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import unicodedata
import json
import urllib

class TwitterObj:

	REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
	AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
	ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

	CONSUMER_KEY = "LyKHJwef85vgzDzYM9Fb9oyzO"
	CONSUMER_SECRET = "Sz1kHAePmWgNN3XgHnihhoVqvvmr6Ock2N031pSGWIZj2HmZJm"

	OAUTH_TOKEN = "104713628-egqwmTA0D92dEPjRPZUd1ifWVZ84d6leYrLeZIdO"
	OAUTH_TOKEN_SECRET = "gSITLiyUdr2eLfPUsFIjAfWgbOi9EQJsm0BgESdwd6MSL"


	def setup_oauth(self):
		"""Authorize your app via identifier."""
		# Request token
		oauth = OAuth1(self.CONSUMER_KEY, client_secret=self.CONSUMER_SECRET)
		r = requests.post(url=self.REQUEST_TOKEN_URL, auth=oauth)
		credentials = parse_qs(r.content)

		resource_owner_key = credentials.get('oauth_token')[0]
		resource_owner_secret = credentials.get('oauth_token_secret')[0]

		# Authorize
		authorize_url = self.AUTHORIZE_URL + resource_owner_key
		print 'Please go here and authorize: ' + authorize_url

		verifier = raw_input('Please input the verifier: ')
		oauth = OAuth1(self.CONSUMER_KEY,
					client_secret=self.CONSUMER_SECRET,
					resource_owner_key=resource_owner_key,
					resource_owner_secret=resource_owner_secret,
					verifier=verifier)

		# Finally, Obtain the Access Token
		r = requests.post(url=self.ACCESS_TOKEN_URL, auth=oauth)
		credentials = parse_qs(r.content)
		token = credentials.get('oauth_token')[0]
		secret = credentials.get('oauth_token_secret')[0]

		return token, secret

	def get_oauth(self):
		oauth = OAuth1(self.CONSUMER_KEY,
					client_secret=self.CONSUMER_SECRET,
					resource_owner_key=self.OAUTH_TOKEN,
					resource_owner_secret=self.OAUTH_TOKEN_SECRET)
		return oauth

	def getTweets(self):
	
		if not self.OAUTH_TOKEN:
			token, secret = self.setup_oauth()
			print "OAUTH_TOKEN: " + token
			print "OAUTH_TOKEN_SECRET: " + secret
			print
		else:
			oauth = self.get_oauth()
			
			#URL 1 -> q = transgender			
			url1 = "https://api.twitter.com/1.1/search/tweets.json?q=transgender&result_type=popular"

			#URL 2 -> q = #MuslimBan from 18 Jan to 18 Feb
			url2 = "https://api.twitter.com/1.1/search/tweets.json?q=%23MuslimBan%20since%3A2017-01-18%20until%3A2017-02-18&result_type=popular"


			#URL 3 -> NASA
			url3 = "https://api.twitter.com/1.1/search/tweets.json?q=NASA&result_type=popular"

			r = requests.get(url=url1, auth=oauth)
			return r.json()
	

