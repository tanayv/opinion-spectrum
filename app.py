
#Inherited from clickbait-repel
from flask import Flask
import json

#getTweets class
from getTweets import *

app = Flask(__name__)

@app.route('/')
def homeDisp():
	x = TwitterObj()
	y = x.getTweets()
	return str(trimData(y))


def trimData(y):
	spectrum = [[0 for xMax in range(7)] for yMax in range(20)]
	for i in range(0, 20):
		spectrum[i][0] = y[i]["text"]
		spectrum[i][1] = y[i]["user"]["name"]
		spectrum[i][2] = y[i]["user"]["screen_name"]
		spectrum[i][3] = y[i]["user"]["verified"]		
		spectrum[i][4] = y[i]["user"]["followers_count"]		
		spectrum[i][5] = y[i]["favorite_count"]
		spectrum[i][6] = y[i]["retweet_count"]

	return spectrum
