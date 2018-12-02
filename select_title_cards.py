# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 09:58:44 2018

@author: Avi Trost
"""
import re
import random

def get_file_name(file_path):
    slash = file_path.rfind("\\")
    dot = file_path.rfind(".")
    return file_path[slash + 1:dot]
    #print(searchObj)
    #return 0

def search(string, title_cards): #return tuple with the best substring and its file path
    '''pattern = "(" #Matches substrings of string
    pattern += string[0]
    for i in range(1,len(string)):
        pattern += string[i] + "?"
    pattern += ")"
    for o in range(1, len(string)):
        pattern += "|("
        for p in range(len(string)):
            if p != o: pattern += string[p] + "?"
            else: pattern += string[p]
        pattern += ")"
    '''
    best = (None, "")
    pattern = "(?!\s*$)("
    for c in string:
        pattern += c + "?"
    pattern += ")"
    pointer = 0
    #pointer = random.randint(0, len(title_cards) - 1) #random initial pointer
    end = pointer
    while(pointer < len(title_cards) and best[1] != len(string)):
        card_text = get_file_name(title_cards[pointer]) #Need a function that gets the title card name
        searchObj = re.findall(str(pattern), str(card_text), re.I) #Check later if this works
        searchObj = list(filter(None, searchObj))
        if len(searchObj) > 0:
            largest_in_card = max(searchObj, key=len)
            if len(largest_in_card) > len(best[1]):
                best = (title_cards[pointer], largest_in_card) #File path and largest substring
        pointer += 1
    pointer = 0
    while(pointer < end and best[1] != len(string)):
        card_text = get_file_name(title_cards[pointer]) #Need a function that gets the title card name
        searchObj = re.findall(str(pattern), str(card_text), re.I) #Check later if this works
        searchObj = list(filter(None, searchObj))
        if len(searchObj) > 0:
            largest_in_card = max(searchObj, key=len)
            if len(largest_in_card) > len(best[1]):
                best = (title_cards[pointer], largest_in_card) #File path and largest substring
        pointer += 1
    complete_list = []
    if(best[1] == string): complete_list.append(best)
    else:
        print(best[1])
        start = string.index(best[1])
        if start != 0:
            complete_list.append(search(string[:start], title_cards))
        complete_list.append(best)
        complete_list.append(search(string[len(best[1]):], title_cards))
    return complete_list
    
    

def select(input_text, title_cards): #will be a list of lists, with 1 word each
    selections = [] #Will contain tuples of (input_text word, (title card, characters to extract from that card))
    for word in input_text.split():
        selections.append(word, search(word, title_cards))
    return selections

title_cards = []
title_cards.append("C:\\Users\\fmcs\\Documents\\BlairHacks2018\\titleCards\\Chimps Ahoy.jpg")
title_cards.append("C:\\Users\\fmcs\\Documents\\BlairHacks2018\\titleCards\\Chocolate with Nuts.jpg")
title_cards.append("C:\\Users\\fmcs\\Documents\\BlairHacks2018\\titleCards\\Clam up!.png")
title_cards.append("C:\\Users\\fmcs\\Documents\\BlairHacks2018\\titleCards\\Clams.jpg")
input_text = "The Ahoy Chocolate Clams"
print(select(input_text, title_cards))
#print(get_file_name("C:\\Users\\fmcs\\Documents\\BlairHacks2018\\titleCards\\Chimps Ahoy.jpg"))