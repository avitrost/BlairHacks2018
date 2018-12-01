'''
Created on Sat Dec 1 2018
@author: Andrew Zhong
'''
import numpy as np
from PIL import Image

def getImages(paths):
  return [Image.open(i) for i in paths]

def merge(img_list, isVertical):
  imgs = getImages(img_list)
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


def arrayMerge(imgArray): #merges 2D array of images
  return vMerge([hMerge(imgArray[0]),hMerge(imgArray[1])])
  #return vMerge([hMerge(row) for row in imgArray])
    
    

#imgs = ["test1.png","test2.png","test4.jpg","test3.png"]
#merge(imgs, False).show()       #open

nameArray = [["test1.png","test4.jpg"],["test2.png","test3.png"]]
imgArray = [getImages(row) for row in nameArray]
arrayMerge(imgArray).show()
