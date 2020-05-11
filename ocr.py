from PIL import Image
import sys
import pyocr
import pyocr.builders
import pytesseract

tools = pyocr.get_available_tools()
tool = tools[0]

def img_to_text(images):
    text_statement = ""
    for image in images:
        text_statement += tool.image_to_string(
            Image.open(image),
            lang='eng',
            builder=pyocr.builders.TextBuilder()
        )
    return text_statement