#Takes the downloaded title cards and maps what the title says to the name of the file

import os

#Path to the file of title cards
folder_path = "C:\\Users\\Avi\\Documents\\BlairHacks2018\\titleCards"
pictures = [f for f in os.listdir(folder_path)]

#Things to change about the titles
swaps = {"%27":"\'","%3F":"?","%26":"&","%C3%A0":"à"}
prefix = {"SB_":12,"SB2":11,"S09":8,"220_Episodenkarte-":18,
          "a_Episodenkarte":19,"b_Episodenkarte":19,"229a_Doodle":5}

postfix = {"_HD":3,"_title_card":11,"_Titlecard":10,"TitleCard":9,
           "_High_Quality":13,"-1":2,"-Titlecard":10,"_Title_Card":11,
           "_Placeholder":12,"_-_Title_Card":13}

complete_swaps = {"073EDFE4-CCF2-4E8E-87CB-25B198F92F0A.jpeg":"No_Pictures_Please.jpeg",
                  "59ED455E-B3A4-4280-AF27-F3380F80F98B.jpeg":"SQUID_NOR.jpeg",
                  "20170610-170130.jpg":"The_Getaway.jpg",
                  "F095AAD9-6113-4809-818F-3FA7B598EBBD.jpeg":"Scavenger_Pants.jpeg",
                  "IMG_5604.png":"Lost and Found.png","C.3-1":"JellyFishing.jpg",
                  "Vlcsnap-2016-10-15-07h31m53s.png":"Whirly_Brians.png",
                  "Vlcsnap-2016-10-29-07h31m11s.png":"MERMAID_PANTS.png",
                  "Vlcsnap-2017-09-27-21h34m05s079.png":"There's_a_Sponge_in_my_soup.png",
                  "Vlcsnap-2017-11-08-21h43m06s.png":"Cuddle_E._Hugs.png"}

#returns the mapping of the writing in the cards to the name of the file
def trueName(pictures):

    mapping = {}
    
    for pic in pictures:
        old_pic = pic
        for key in swaps:
            pic = pic.replace(key,swaps[key])
        for key in prefix:
            if key in pic:
                pic = pic[prefix[key]:]
        for key in postfix:
            if key in pic:
                picSplit = pic.split(".")
                pic = picSplit[0]
                pic = pic[:len(pic) - postfix[key] - 1]
                pic += "." + picSplit[1]
        for key in complete_swaps:
            if key == pic:
                pic = complete_swaps[key]

        pic = pic.replace("_"," ")
        mapping[pic] = old_pic

    return mapping

#writes the information in a text file
things = trueName(pictures)
file = open("mapping.txt","w+")
for title in things:
    file.write(title + " = " + things[title] + "\n")
file.close()
