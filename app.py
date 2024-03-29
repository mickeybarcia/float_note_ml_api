from flask import Flask, jsonify, request, abort
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import requests
import datetime
import pprint
import time
import random
import os
import time
import sys 
import traceback

from keywords import text_to_keywords
import summary
from ocr import img_to_text
from sentiment import text_to_sentiment

load_dotenv()
app = Flask(__name__)
api_key = os.environ.get("API_KEY")
img_subscription_key = os.environ.get("IMG_SUBSCRIPTION_KEY")
text_subscription_key = os.environ.get("TEXT_SUBSCRIPTION_KEY")

@app.route('/')
def index():
	return "you've reached the floatie ML API! congrats!"

def check_auth(headers):
	try:
		token = headers.get("authorization")
		if token != "Bearer " + api_key:
			abort(401)
	except:
		abort(401)

@app.errorhandler(Exception)
def handle_error(e):
    traceback.print_tb(e.__traceback__)
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

@app.route('/entry-image', methods = ['POST'])
def generate_entry_ml_from_image():
	check_auth(request.headers)
	images = request.files.getlist("page")
	start_time = time.time() 
	text = img_to_text(images, img_subscription_key)
	if not text:
		raise Exception('Unable to extract text')
	image_time = time.time() 
	
	if request.args.get('analyze') == "1":
		score = text_to_sentiment(text, text_subscription_key)
		score_time = time.time() 
		
		keywords = text_to_keywords(text)
		keyword_time = time.time()

		# print('keyword time: ' + str(keyword_time - score_time))
		print('score gen time: ' + str(score_time - image_time))
		print('image text gen time: ' + str(image_time - start_time))
		return jsonify({"text": text, "score": score, "keywords": keywords})
	else:
		return jsonify({"text": text})

@app.route('/entry-text', methods = ['POST'])
def generate_entry_ml_from_text():
	check_auth(request.headers)
	entry_data = request.json
	text = entry_data["text"]
	score = text_to_sentiment(text, text_subscription_key)
	keywords = text_to_keywords(text)
	return jsonify({"text": text, "score": score, "keywords": keywords})

@app.route('/summary', methods = ["POST"])
def get_summary():
	check_auth(request.headers)
	summary_data = request.json
	summary_text = summary.get_summary(summary_data["text"])
	return jsonify({"summary": summary_text})	

if __name__ == "__main__":
	for ex in default_exceptions:
		app.register_error_handler(ex, handle_error)
	app.run(debug=True, use_debugger=True)