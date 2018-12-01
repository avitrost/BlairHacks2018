'''
Created on Sat Dec 1 2018
@author: Andrew Zhong
Requires numpy and PIL (pillow)
'''
import numpy as np
from PIL import Image

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

  x,y = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1] #gets size of smallest image as tuple x,y

  new = np.hstack((np.asarray(i.resize((int(i.size[0] * (y/i.size[1])),y))) for i in imgs))    #images have to be of equal size to combine

  new = Image.fromarray(new)          #image from vertical array of images
  return new


def arrayMerge(imgPaths): #takes array of paths and merges 2D array of images
  imgArray = [getImages(row) for row in imgPaths]
  return vMerge([hMerge(imgArray[0]),hMerge(imgArray[1])])

#Testing of arrayMerge
pathArray = [["test1.png","test4.jpg"],["test2.png","test3.png"]]
arrayMerge(pathArray).show()
