import urllib.request
import re
import json
import os
import random
import time

from config.py import NEWSAPI_KEY

def sinput(prompt):
    return input(prompt).strip()

# ask http request for the url
def request(url, queryDict):
    if queryDict !=None:
        url += "?" 
        for query in queryDict:
            url += query + "=" + queryDict[query] + "&"
    res = urllib.request.urlopen(url)
    statusCode = res.getcode()
    if statusCode == 200:
        return res.read().decode('utf-8')
    return None

def newsapijson(url, source, sortBy, apiKey, order):
    queryDict = {
        "source" : source,
        "sortBy" : sortBy,
        "apiKey" : apiKey
    }
    res = request(url, queryDict)
    if res ==None:
        print("-Please check your internet environment.-")
        return None, None
    res = json.loads(res)
    newsUrl = res["articles"][order]["url"]
    title = res["articles"][order]["title"]
    return newsUrl, title

def TheNextWebHtml(order):
    url = "https://newsapi.org/v1/articles"
    source = "the-next-web"
    sortBy = "latest"
    apiKey = NEWSAPI_KEY
    TNWNewsUrl, title = newsapijson(url, source, sortBy, apiKey, order)
    if not TNWNewsUrl:
        return None, None
    html = urllib.request.urlopen(TNWNewsUrl).read().decode("utf8").replace(u'\xa0', u' ').replace(u'\u2014', u' ').replace(u'\u2013', u' ')
    return html.split('<meta property="bt:body" content="')[1].split('">')[0], title

def ArsTechnicaHtml(order): # not completed code
    url = "https://newsapi.org/v1/articles" 
    source = "ars-technica"
    sortBy = "top"
    apiKey = NEWSAPI_KEY
    ATNewsUrl, title = newsapijson(url, source, sortBy, apiKey, order)
    if not ATNewsUrl:
        return None, None

def divideIntoSentence(content):
    sentences = re.finditer(r"\S[^\.]+\.", content)
    return sentences

def subBlank(sentence, wordList):
    def stringsToBeMatched(wordList):
        for word in wordList:
            checkingString = word + "\W"
            if not word[0].isupper():
                checkingString = "\W" + checkingString
            yield word, checkingString
    ans = []
    for word, checkingString in stringsToBeMatched(wordList):
        temp =[(idx, word) for idx in (m.start() for m in re.finditer(checkingString, sentence))]
        ans.extend(temp)
    ans.sort(reverse=True)
    answer = []
    for n, word in enumerate(ans):
        idx = word[0]
        word = word[1]
        idxofend = idx+len(word)
        if not word[0].isupper():
            idx += 1
            idxofend += 1
        sentence = sentence[:idx] + "(" + str(len(ans)-n) + ".___)" + sentence[idxofend:]
        answer.insert(0, word)
    return (answer, sentence)

def end(*args):
    print("\n-The Practice Terminated.-\n")
    return "end"

def clear(*args):
    os.system("clear")
    return "clear"

def incorrect(*args):
    replyIncorrect = ["No.", "Nope."]
    print(random.choice(replyIncorrect))
    return "incorrect"

def noIdea(ans):
    print(ans)
    return "noIdea"

def correct(ans):
    return "correct"

def blankQuiz(targetWords):
    print("Getting an article to exercise from The Next Web....")
    content, title = TheNextWebHtml(0) ########### the order decision
    if content == None:
        return None
    print("\n<{}>".format(title)) # title
    sentenceList = divideIntoSentence(content)
    time.sleep(2)
    for n,sentence in enumerate(sentenceList):
        sentence = sentence.group(0).strip()
        (answer, sentenceWithBlank) = subBlank(sentence, targetWords)
        print("\n#{}:".format(n+1))
        print(sentenceWithBlank)
        print("-"*len(sentenceWithBlank)+"\n")
        if not answer:
            print("**There is no articles. move onto next sentence after 3 seconds.")
            time.sleep(3)
            continue
        for n,ans in enumerate(answer):
            ansSet = {
                "exit" : end,
                "end" : end,
                "?" : noIdea,
                "clear" : clear,
                ans : correct
            }
            reply = sinput("answer"+str(n+1)+" : ")
            while not reply in ansSet or reply == "clear":
                if reply == "clear": clear()
                else: incorrect()
                reply = sinput("answer"+str(n+1)+" : ")
            result = ansSet[reply]
            reply = result(ans)
            if reply in ["exit", "end"]:
                return

# article practice by The Times           
def article(argv):
    blankQuiz(["a", "an", "the", "The", "A", "An"])
  
# preposition practice by The Times
def preposition(argv):
    prepositionList = ["in", "on", "up", "at", "with", "over", "without", "toward", "to", 
"forward", "by", "into", "onto", "upto", "down", "for", "about", "of", "along", 
"from", "around", "inside", "upon", "off", "out", "through", "under", "within"]
    prepositionList.extend([s[0].upper()+s[1:] for s in prepositionList]) # strings starting with uppercases
    blankQuiz(prepositionList)    