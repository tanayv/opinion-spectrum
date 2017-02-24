
#Inherited from clickbait-repel
from flask import Flask

#getTweets class
from getTweets import *

app = Flask(__name__)

@app.route('/')
def homeDisp():
	x = TwitterObj()
	str1 = ''.join(str(e) for e in x.getTweets())
	return str1
