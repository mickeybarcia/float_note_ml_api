from PIL import Image
import sys
import pyocr
import pyocr.builders
import time
import requests

vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v1.0/"
text_recognition_url = vision_base_url + "recognizeText"

# tools = pyocr.get_available_tools()
# tool = tools[0]

# def img_to_text(images):
#     text_statement = ""
#     for image in images:
#         text_statement += tool.image_to_string(
#             Image.open(image),
#             lang='eng',
#             builder=pyocr.builders.TextBuilder()
#         )
#     return text_statement

def img_to_text(images, img_subscription_key):
    text_statement = ""
    headers = {'Ocp-Apim-Subscription-Key': img_subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {"mode": "Handwritten"}
    for image in images:
        try:
            response = requests.post(text_recognition_url, headers=headers, params=params, data=image)
            analysis = {}
            while "recognitionResult" not in analysis:
                response_final = requests.get(response.headers["Operation-Location"], headers=headers)
                analysis = response_final.json()
                # time.sleep(0.5)
            polygons = [line["text"] for line in analysis["recognitionResult"]["lines"]]
            text_statement += " ".join(polygons)
        except:
            text_statement += ""
    return text_statement