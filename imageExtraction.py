# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 22:44:07 2018

@author: Tejas Guha
"""

import urllib

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