import urllib.request
import json
import Articles
import re
import sys

def sinput(prompt):
    return input(prompt).strip()

def extractbtw(html, startCriteria, endCriteria):
    reg = re.compile(startCriteria + "((?:(?!" + startCriteria + "|" + endCriteria + ")\W|\w)+)" + endCriteria)
    result = [rawMeaning.group(1) for rawMeaning in re.finditer(reg, html)]
    return result

def erasewithregex(string,*args):
    for pattern in args:
        string = re.sub(re.compile(pattern), "", string)
    return string

def searchInDaumDict(term):
    print("Getting the meanings from http://dic.daum.net....")    
    url = "http://dic.daum.net/search.do"
    queryString={
        "q" : term.replace(" ","%20") # space
    }
    # meanings
    res = Articles.request(url, queryString).replace(u'\u03ac', u'')
    confinedHTML = extractbtw(res, '<ul class="list_search">', '</ul>')
    if not confinedHTML: 
        return ([],[])
    rawMeanings = extractbtw(confinedHTML[0], '<span class="txt_search">', '</span>')
    result = (erasewithregex(rawMeaning, '<daum:word id="[^<>]+">', '</daum:word>') for rawMeaning in rawMeanings)
    # Found word
    word = extractbtw(res,'class="txt_cleansch"><span class="txt_emph1">', '</span>')
    word = " ".join(word) # 1. word must be a list had one element. 2. if word is empty, then just it can be an empty string.
    return (word, result)

def search(term):
    (word, meaninglist) = searchInDaumDict(term)
    if not meaninglist:
        print("NOT FOUND")
        return
    print("\n"+word)
    for meaning in meaninglist:
        if meaning != "":
            print(meaning)
    print("")

# search a meaning of a word at dictionaries
def reference(argv):
    if argv:
        term = " ".join(argv)
        return search(term)
    print("Search Mode Start\n")
    term = sinput("Search$ ")
    while not term in ["exit", "end"]:
        search(term)
        term = sinput("Search$ ")

