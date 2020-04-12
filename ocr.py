from PIL import Image
import sys
import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
tool = tools[0]
langs = tool.get_available_languages()
lang = langs[0]

def img_to_text(images):
    text_statement = ""
    for image in images:
        text_statement += tool.image_to_string(
            Image.open(image),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
    return text_statement