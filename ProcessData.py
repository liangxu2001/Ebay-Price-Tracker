import re
"""
Everything in this file is ment to do metrics on a list of data
List of data include the following feilds for the dictonary:

'title': 
'soldprice': 
'link': 
'date': 

"""

#Given a list of dict, we will return the average of all the soldprice
def getAverage(list):
    if len(list) == 0:
        return 0 
    
    sum = 0
    for data in list:
        sum += data["soldprice"]
    return sum / len(list)

#Goes through the dictonary and removes any words from the title that we don't want
def requiredWords(list, keywords):
    newList = []
    for listing in list:
        title = listing['title']

        #If we have a negative hit, abandon listing and move to the next one
        negativeHit = False
        for word in keywords:
            if word.lower() not in title.lower():
                negativeHit = True
                break
        
        if negativeHit:
            continue

        newList.append(listing)
    
    return newList

def remove_emojis(string):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', string)

#Print all of the listings found into text file
def saveList(list):
    with open('logs.txt', 'w') as f:
        for listing in list:
            writeString = str(listing['soldprice']) + '\t' + listing['title'] +'\t' + listing['link'] + '\n'
            f.writelines(remove_emojis(writeString))