'''
Created on Sat Dec 1 2018
@author: Andrew Zhong
'''
import numpy as np
from PIL import Image

def Merge(img_list, isVertical):
  if isVertical:
    return VMerge(img_list)
  else:
    return HMerge(img_list)

def VMerge(img_list): #img_list: string array of image paths

  imgs = [Image.open(i) for i in img_list]

  x,y = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1] #gets size of smallest image as tuple x,y

  new = np.vstack((np.asarray(i.resize((x, int(i.size[1] * (x/i.size[0]))))) for i in imgs))    #images have to be of equal size to combine

  new = Image.fromarray(new)          #image from vertical array of images
  new.save('test.png')
  return new

def HMerge(img_list): #img_list: string array of image paths

  imgs = [Image.open(i) for i in img_list]

  x,y = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1] #gets size of smallest image as tuple x,y

  new = np.hstack((np.asarray(i.resize((int(i.size[0] * (y/i.size[1])),y))) for i in imgs))    #images have to be of equal size to combine

  new = Image.fromarray(new)          #image from vertical array of images
  new.save('test.png')
  return new

imgs = ["test1.png","test2.png","test3.png"]

Merge(imgs, True).show()       #open 

