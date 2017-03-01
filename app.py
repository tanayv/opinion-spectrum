
#Inherited from clickbait-repel
from flask import Flask, render_template, request, redirect, url_for
import json
from textblob import TextBlob

#getTweets class
from getTweets import *

app = Flask(__name__)


@app.route('/')
def begin():
	return render_template('start.html')


@app.route('/create')
def homeDisp():
	query = request.args.get('query')
	x = TwitterObj()
	y = x.getTweets(query)
	z = trimData(y)
	return render_template('main.html', grid=visualize(z))

def trimData(y):
	spectrum = [[0 for xMax in range(10)] for yMax in range(14)]
	for i in range(0, 14):
		spectrum[i][0] = y["statuses"][i]["text"]
		spectrum[i][1] = y["statuses"][i]["user"]["name"]
		spectrum[i][2] = y["statuses"][i]["user"]["screen_name"]
		spectrum[i][3] = y["statuses"][i]["user"]["verified"]		
		spectrum[i][4] = y["statuses"][i]["user"]["followers_count"]		
		spectrum[i][5] = y["statuses"][i]["favorite_count"]
		spectrum[i][6] = y["statuses"][i]["retweet_count"]

		#Sentiment Analysis with weightage calculation for polarity and subjectivity
		wiki = TextBlob(spectrum[i][0])
		spectrum[i][7] = wiki.sentiment.polarity * (1 + 0.5*wiki.sentiment.subjectivity)
		
		#Reliability Rating
		if spectrum[i][3] == True:
			vfied = 0.5

		else:
			vfied = 0
		
		#clickbait = clickbait(spectrum[i][0])  // b/w -0.2 to 0.2
		clickbait = 0

		#sourcerep = sourcerep(spectrum[i][0])  // b/w -0.2 to 0.2
		sourcerep = 0.2

		spectrum[i][8] = vfied + sourcerep + clickbait 
		# --- End of reliability rating

		
		#Reach/Influence Rating
		spectrum[i][9] = (0.1 * int(spectrum[i][4])) + (1 * int(spectrum[i][5])) + (1.2 * int(spectrum[i][5]))

				
	return spectrum


def visualize(spectrum):
	

	#SORTING
	#Declare all intervals on x-axis
	extNeg = []
	neg = []
	neu = []
	pos = []
	extPos = []


	#loop through the spectrum
	for i in range(0, 14):
	
		#append i and reliability value to interval
		info = []
		info.append(i)
		info.append(spectrum[i][8])

		rel = spectrum[i][7]

		if (rel >= -1 and rel < -0.2):
			extNeg.append(info)

		elif (rel >= -0.2 and rel < -0.01):
			neg.append(info)

		elif (rel >= -0.01 and rel < 0.1):
			neu.append(info)	

		elif (rel >= 0.1 and rel < 0.5):
			pos.append(info)

		elif (rel >= 0.5):
			extPos.append(info)

	#CHECK SORTING 
	#print "Extremely Negative: " + str(extNeg)			
	#print "Negative: " + str(neg)
	#print "Neutral: " + str(neu)
	#print "Positive: " + str(pos)
	#print "Extremely Positive: " + str(extPos)


	extNeg.sort(key = lambda x:info[1])
	neg.sort(key = lambda x:info[1])
	neu.sort(key = lambda x:info[1])
	pos.sort(key = lambda x:info[1])
	extPos.sort(key = lambda x:info[1])

	#print "-------------------------------- After Sorting"
	#print "Extremely Negative: " + str(extNeg)			
	#print "Negative: " + str(neg)
	#print "Neutral: " + str(neu)
	#print "Positive: " + str(pos)
	#print "Extremely Positive: " + str(extPos)



	#RENDERING
	str1 = "<div class='grid'>"

	str1 += "<div class='col extNeg'> <div class='card'><b>Extremely Negative</b></div>"
	
	for card in extNeg:
		i = card[0]
		strCD = "<div class='card'><b>" + spectrum[i][1] + "</b><i>@" + spectrum[i][2] + "</i><br>" + spectrum[i][0] + "<hr>Sentiment: " + str(spectrum[i][7]) + "<br>Reach Estimate: " + str(spectrum[i][9]) + "</div>"
		str1 += strCD	
	str1 += "</div>"	 

	str1 += "<div class='col neg'> <div class='card'><b>Negative</b></div>"
	for card in neg:
		i = card[0]
		strCD = "<div class='card'><b>" + spectrum[i][1] + "</b><i>@" + spectrum[i][2] + "</i><br>" + spectrum[i][0] + "<hr>Sentiment: " + str(spectrum[i][7]) + "<br>Reach Estimate: " + str(spectrum[i][9]) + "</div>"
		str1 += strCD	
	str1 += "</div>"	 
	

	str1 += "<div class='col neu'> <div class='card'><b>Neutral</b></div>"	
	for card in neu:
		i = card[0]
		strCD = "<div class='card'><b>" + spectrum[i][1] + "</b><i>@" + spectrum[i][2] + "</i><br>" + spectrum[i][0] + "<hr>Sentiment: " + str(spectrum[i][7]) + "<br>Reach Estimate: " + str(spectrum[i][9]) + "</div>"
		str1 += strCD	
	str1 += "</div>"

	
	str1 += "<div class='col pos'> <div class='card'><b>Positive</b></div>"	
	for card in pos:
		i = card[0]
		strCD = "<div class='card'><b>" + spectrum[i][1] + "</b><i>@" + spectrum[i][2] + "</i><br>" + spectrum[i][0] + "<hr>Sentiment: " + str(spectrum[i][7]) + "<br>Reach Estimate: " + str(spectrum[i][9]) + "</div>"
		str1 += strCD	
	str1 += "</div>"

	str1 += "<div class='col extPos'> <div class='card'><b>Extremely Positive</b></div>"	
	for card in extPos:
		i = card[0]
		strCD = "<div class='card'><b>" + spectrum[i][1] + "</b><i>@" + spectrum[i][2] + "</i><br>" + spectrum[i][0] + "<hr>Sentiment: " + str(spectrum[i][7]) + "<br>Reach Estimate: " + str(spectrum[i][9]) + "</div>"
		str1 += strCD	
	str1 += "</div>"	 
	 
	#End of Grid 

	str1 += "</div>"
	

	return str1









