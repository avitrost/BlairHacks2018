from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from tkinter.filedialog import askopenfilename
import requests
from PIL import Image
from io import BytesIO
import time
from tkinter import *
from tkinter import ttk
import numpy as np
import os
import re
from random import *
from PIL import Image
import urllib
import csv

#Image Extraction ------------------------------------------------------------------------------------------------------------------------
def downloadCards():
	web = urllib.urlopen('http://spongebob.wikia.com/wiki/List_of_title_cards')
	html = web.read()
	index = html.find("wiki/File:")
	while (index != -1):
		end = html.find('"', index+1)
		imageUrl = html[index:end]
		name = imageUrl[imageUrl.find(":")+1:]
		imageHTML = urllib.urlopen("http://spongebob.wikia.com/"+imageUrl).read()
		imageStart = imageHTML.find('og:image" content="')+len('og:image" content="')
		imageEnd = imageHTML.find('"', imageStart+1)
		urllib.urlretrieve(imageHTML[imageStart:imageEnd], "titleCards/"+name)
		index = html.find("wiki/File:", end + 1)


#OCR -------------------------------------------------------------------------------------------------------------------------------------

subscription_key = 'be5f1724e29e451e89fba43668c60cd2'
assert subscription_key

vision_base_url = 'https://eastus.api.cognitive.microsoft.com/vision/v2.0/'

ocr_url = vision_base_url + "RecognizeText"

headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
params  = {'mode':'Printed'}

#Azure Computer Vision Text Recognition
#https://engmrk.com/handwritten-text-from-images-azure/
#https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/587f2c6a154055056008f200
#Azure login
#guhatejas@gmail.com
#Mun6169114

# Extract the word bounding boxes and text.
def getSnippets(image_path):
	image_data = open(image_path, "rb").read()
	response = requests.request('post', ocr_url, headers=headers, params=params, data=image_data)
	operationLocation = response.headers["Operation-Location"]
	analysis,lines = None,None
	done = False
	while not done:
		try:
			analysis = requests.request('get', operationLocation, json=None, data=None, headers=headers, params=None).json()
			lines = analysis["recognitionResult"]['lines']
			done = True
		except: time.sleep(1)
			
	return lines

#Image merging -----------------------------------------------------------------------------------------------------

def getImage(path):
  return Image.open(path)

def getImages(paths):
  return [Image.open(i) for i in paths]

def merge(imgPaths, isVertical):  #img_list: array of pathnames
  imgs = getImages(imgPaths)
  if isVertical:
	return vMerge(imgs)
  else:
	return hMerge(imgs)


def vMerge(imgs): #img_list: array of images
  
  if len(imgs) == 0:
	raise ValueError('No images found')
	return
  if len(imgs) == 1:
	return imgs[0]

  x,y = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1] #gets size of smallest image as tuple x,y

  new = np.vstack((np.asarray(i.resize((x, int(i.size[1] * (x/i.size[0]))))) for i in imgs))    #images have to be of equal size to combine

  new = Image.fromarray(new)          #image from vertical array of images
  return new

def crop(string, image_path):
    im = Image.open(image_path)
    image_data = open(image_path, "rb").read()
    response = requests.request('post', ocr_url, headers=headers, params=params, data=image_data)
    operationLocation = response.headers["Operation-Location"]
    analysis,lines = None,None
    done = False
    while not done:
        try:
            analysis = requests.request('get', operationLocation, json=None, data=None, headers=headers, params=None).json()
            lines = analysis["recognitionResult"]['lines']
            done = True
        except: time.sleep(1)
    for i in range(len(lines)):
        words = lines[i]["words"]
        for j in range(len(words)):
            tl = (words[j]['boundingBox'][0], words[j]['boundingBox'][1]) #coords of boxes
            tr = (words[j]['boundingBox'][2], words[j]['boundingBox'][3])
            br = (words[j]['boundingBox'][4], words[j]['boundingBox'][5])
            bl = (words[j]['boundingBox'][6], words[j]['boundingBox'][7])
            text = words[j]['text'] #the word it is
            if text == string:
                return im.crop((tl[0]-40, tr[1]-20, br[0]+40, bl[1]+20))

def hMerge(imgs): #img_list: array of images

  if len(imgs) == 0:
	raise ValueError('No images found')
	return
  if len(imgs) == 1:
	return imgs[0]

  x,y = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1] #gets size of smallest image as tuple x,y

  new = np.hstack((np.asarray(i.resize((int(i.size[0] * (y/i.size[1])),y))) for i in imgs))    #images have to be of equal size to combine

  new = Image.fromarray(new)          #image from vertical array of images
  return new


def arrayMerge(imgPaths): #takes array of paths and merges 2D array of images
  imgArray = [getImages(row) for row in imgPaths]
  return vMerge([hMerge(imgArray[0]),hMerge(imgArray[1])])

def getPath(char):    #gets path to random matching character
  letters = os.listdir("Texts")
  
  specialCharMap = {"'":"APOSTROPHE","?":"QUESTIONMARK","!":"EXCLAIMATION","-":"HYPHEN",".":"PERIOD",",":"COMMA"}
  if char in specialCharMap:
	char = specialCharMap[char]
	
  path = "Texts/" + char.upper() + "_1"
  if not char.upper() + "_1.PNG" in letters:
	print(path)
	raise ValueError("Character not found")
  
  same = [path + ".PNG"]
  for name in letters:
	if re.match(char.upper() + "_\d.PNG",name):
	  same.append("Texts/" + name)
  path = same[int(random() * len(same))]
  return path

def spellWord(string):
  return hMerge(getImages([getPath(char) for char in string]))

try: mapping = read()
except: raise ValueError("Mapping not found")

def getWord(string):
    global mapping
    temp = string
    while not temp in mapping:
        temp = temp[:-1]
        if len(string) <= 1:
            return spellWord(string)
    possible = mapping[temp]
    tempImg = None
    if temp == string:
        tempImg = spellWord(string[len(temp):])
    return hMerge(crop(string,possible[math.random*len(possible)]),tempImg)

def lastLine(string,width):   #calculates how many character would be in the last line of textBox
  charLen = 0
  for s in string.split():
	if charLen < width:
	  charLen += len(s)
	else:
	  charLen = 0
  return charLen


def calcWidth(string,maxLines,tolerance):      #Calculates width based on a maximum number of lines for textBox
  #remove whitespace
  strings = string.strip().split(' ')
  while '' in strings:
	strings.remove('')
  charCount = len(string.strip().replace(' ',''))

  #increment width until last line is within tolerable range
  maxWidth = charCount//maxLines
  while lastLine(string,maxWidth) < maxWidth * tolerance:    #checks if last line is within tolerable range of maxWidth
	maxWidth += 1
  return maxWidth

def textBox(string, maxLines = 5, tolerance = 0.5):
  if len(string) == 0:
	raise ValueError('No Text provided')
  maxWidth = calcWidth(string,maxLines,tolerance)
  lines = []  #array of lines
  line = []   #array of word images
  charLen = 0
  strings = string.strip().split()
  for string in strings:  #fills line with words until empty, then vMerges
	if charLen < maxWidth:
	  line.append(spellWord(string))
	  charLen += len(string)
	else:
	  lines.append(hMerge(line))
	  line = []
	  line.append(getWord(string))
	  charLen = len(string)
  if(len(line) != 0):
	lines.append(hMerge(line))
  return vMerge(lines)

#Word Mapping Generator -----------------------------------------------------------------------------------------

def genWordMapping(folder):
	mapping = {}
	files = os.listdir(folder)
	for img in files:
		path = folder + "/" + img
		print(path)
		try:
			lines = getSnippets(path)
			im = Image.open(path)
			for i in range(len(lines)):
				words = lines[i]["words"]
				for j in range(len(words)):
					tl = (words[j]['boundingBox'][0], words[j]['boundingBox'][1]) #coords of boxes
					tr = (words[j]['boundingBox'][2], words[j]['boundingBox'][3])
					br = (words[j]['boundingBox'][4], words[j]['boundingBox'][5])
					bl = (words[j]['boundingBox'][6], words[j]['boundingBox'][7])
					text = words[j]['text'] #the word it is
					if text.lower() in img.lower():
						if not text in mapping:
							mapping[text] = [img]
						else:
							mapping[text].append(img)
		except:
			print('Error with ' + path)
				#im.crop((tl[0], tr[1], br[0], bl[1])).save("first.jpg")    
	with open('wordLocations.csv', mode='w') as locations:
		writer = csv.writer(locations, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for word in mapping:
			writer.writerow([word.lower()] + mapping[word])
	print("done")

#Reading from CSV---------------------------------------------------------------------------
def read():
	with open('wordLocations.csv', mode='r') as infile:
	reader = csv.reader(infile)
	mapping = {rows[0]:rows[1:] if len(rows[0]) > 1 else continue for rows in reader}
	return mapping
def merge():
	vMerge([getImage("top.PNG"),textBox("Spongebob is great boi",3,0.8)]).show()

#main ----------------------------------
#genWordMapping("titleCards")

class GUI:
    def __init__(self, root):
        self.v = StringVar()
        self.root = root
        root.title("Spongebob meme generator")
        self.file_button = Button(root, text = "Select Background Picture", width = 55, command=self.ask_for_file)
        self.file_button.pack()
        self.label = Label(root, text = "Text: ", width = 10)
        self.label.pack()
        self.entry = Entry(root,width = 30, textvariable=self.v)
        self.entry.pack()
        self.button = Button(root,text = "GENERATE",width = 55, command=self.merge)
        self.button.pack()
        self.v.set("")
    def ask_for_file(self):
        file = askopenfilename(filetypes=(("Template files", "*.tplate"),
                                           ("HTML files", "*.html;*.htm"),
                                           ("All files", "*.*") ))
        if file != None:
            return file
        print("Error with file")
        return None
    def merge(self):
        vMerge([getImage("top.PNG"),textBox(v.get(),3,0.8)]).show()
r = Tk()
gui = GUI(r)
r.mainloop()
