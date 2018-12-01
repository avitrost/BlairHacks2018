'''
Created on Sat Dec 1 2018
@author: Andrew Zhong
Requires numpy and PIL (pillow)
'''
import numpy as np
import os
import re
from random import *
from PIL import Image

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
      line.append(spellWord(string))
      charLen = len(string)
  if(len(line) != 0):
    lines.append(hMerge(line))
  return vMerge(lines)

vMerge([getImage("top.PNG"),textBox("When Avi whips it out",3,0.8)]).show()
