from PIL import Image
import sys
import pyocr
import pyocr.builders
import time
import requests

vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v3.1/"
text_recognition_url = vision_base_url + "ocr?language=unk&detectOrientation=true"

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
    lines = []
    headers = {'Ocp-Apim-Subscription-Key': img_subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {"mode": "Handwritten"}
    for image in images:
        try:
            response = requests.post(text_recognition_url, headers=headers, params=params, data=image)
            for region in response.json()["regions"]:
                for line in region["lines"]:
                    words = []
                    for word in line["words"]:
                        words.append(word["text"])
                    lines.append(' '.join(words))
        except:
            print('Unable to extract text from image ' + image.filename)
    return '\n'.join(lines) if len(lines) > 0 else None