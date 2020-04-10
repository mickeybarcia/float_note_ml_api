from flask import Flask, jsonify, request, abort
import requests
import datetime
import pprint
import time
import random
from aylienapiclient import textapi
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('config.py')

api_key = os.environ.get("API_KEY")
aylien_app_id = os.environ.get("AYLIEN_APP_ID")
aylien_key = os.environ.get("AYLIEN_KEY")
text_subscription_key =  os.environ.get("TEXT_SUBSCRIPTION_KEY")
img_subscription_key = os.environ.get("IMG_SUBSCRIPTION_KEY")

vision_base_url = app.config["VISION_BASE_URL"]
text_analytics_base_url = app.config["TEXT_ANALYTICS_BASE_URL"]
text_recognition_url = vision_base_url + "recognizeText"
text_client = textapi.Client(aylien_app_id, aylien_key)

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

@app.route('/entry-image', methods = ['POST'])
def generate_entry_ml_from_image():
	check_auth(request.headers)
	images = request.files.getlist("page")
	text = img_to_text(images)
	if request.args.get('analyze') == "1":
		print("analyzing images")
		score = text_to_sentiment(text)
		keywords = text_to_keywords(text)
		return jsonify({"text": text, "score": score, "keywords": keywords})
	else:
		print("just getting the text")
		return jsonify({"text": text})

@app.route('/entry-text', methods = ['POST'])
def generate_entry_ml_from_text():
	check_auth(request.headers)
	entry_data = request.json
	text = entry_data["text"]
	score = text_to_sentiment(text)
	keywords = text_to_keywords(text)
	return jsonify({"text": text, "score": score, "keywords": keywords})

@app.route('/summary', methods = ["POST"])
def get_summary():
	check_auth(request.headers)
	summary_data = request.json
	document = {"text": summary_data["text"], "sentences_number": summary_data["numSentences"], "title": "journal"}
	summary_resp = text_client.Summarize(document)
	summary = " ".join(summary_resp["sentences"])
	return jsonify({"summary": summary})	

def text_to_sentiment(text):
	sentiment_api_url = text_analytics_base_url + "sentiment"
	documents = {"documents": [{"id": "1", "language": "en", "text": text}]}
	headers = {"Ocp-Apim-Subscription-Key": text_subscription_key}
	response = requests.post(sentiment_api_url, headers=headers, json=documents)
	sentiments = response.json()
	score = sentiments["documents"][0]["score"]
	print("score " + str(score))
	return score

def text_to_keywords(text):
	key_phrase_api_url = text_analytics_base_url + "keyPhrases"
	documents = {"documents": [{"id": "1", "language": "en", "text": text}]}
	headers = {"Ocp-Apim-Subscription-Key": text_subscription_key}
	response = requests.post(key_phrase_api_url, headers=headers, json=documents)
	key_phrases = response.json()
	keywords = key_phrases["documents"][0]["keyPhrases"]
	print("keywords " + str(keywords))
	return keywords

def img_to_text(images):
	text_statement = ""
	headers = {'Ocp-Apim-Subscription-Key': img_subscription_key,
              'Content-Type': 'application/octet-stream'}
	params = {"mode": "Handwritten"}
	for image in images:
		try:
			response = requests.post(text_recognition_url, headers=headers, params=params, data=image)
			analysis = {}
			while "recognitionResult" not in analysis:
				response_final = requests.get(response.headers["Operation-Location"], headers=headers)
				analysis = response_final.json()
				time.sleep(1)
			polygons = [line["text"] for line in analysis["recognitionResult"]["lines"]]
			text_statement += " ".join(polygons)
		except:
			text_statement += ""
	return text_statement

if __name__ == "__main__":
	app.run(debug = True)