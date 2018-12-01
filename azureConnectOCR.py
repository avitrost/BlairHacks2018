# -*- coding: utf-8 -*-
"""
Created on Sat Dec 01 15:08:31 2018

@author: Tejas Guha
"""

import requests
from PIL import Image
from io import BytesIO
import time

subscription_key = 'be5f1724e29e451e89fba43668c60cd2'
assert subscription_key

vision_base_url = 'https://eastus.api.cognitive.microsoft.com/vision/v2.0/'

ocr_url = vision_base_url + "RecognizeText"

# Set image_url to the URL of an image that you want to analyze.

headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
params  = {'mode':'Printed'}

#Azure Computer Vision Text Recognition
#https://engmrk.com/handwritten-text-from-images-azure/
#https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/587f2c6a154055056008f200
#Azure login
#guhatejas@gmail.com
#Mun6169114

# Extract the word bounding boxes and text.
def getSnippets(image_path, character):
    image_path = 'titleCards/Born_to_be_Wild.png'
    im = Image.open(image_path)
    character = "BORN"
    image_data = open(image_path, "rb").read()
    response = requests.request('post', ocr_url, headers=headers, params=params, data=image_data)
    operationLocation = response.headers["Operation-Location"]
    time.sleep(5)
    analysis = requests.request('get', operationLocation, json=None, data=None, headers=headers, params=None).json()
    lines = analysis["recognitionResult"]['lines']
    for i in range(len(lines)):
        words = lines[i]["words"]
        for j in range(len(words)):
            tl = (words[j]['boundingBox'][0], words[j]['boundingBox'][1]) #coords of boxes
            tr = (words[j]['boundingBox'][2], words[j]['boundingBox'][3])
            br = (words[j]['boundingBox'][4], words[j]['boundingBox'][5])
            bl = (words[j]['boundingBox'][6], words[j]['boundingBox'][7])
            text = words[j]['text'] #the word it is
            im.crop((tl[0]-20, tr[1]+20, br[0], bl[1])).save("first.jpg") #

getSnippets("l","c")     