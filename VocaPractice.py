import os
import time
import random
import platform
import Articles
import Reference

# global values
DBname = "VocaList.VL"
vocaList = []
division = "|"

# use of English-Korean conversion
if platform.system() == "Windows":
    import HardwareInterrupt
    enterKey = HardwareInterrupt.enterKey
    VK_HanYoung = HardwareInterrupt.VK_HanYoung
    vocaDB = '/'.join(os.path.realpath(__file__).split('\\')[:-1]) + "/"+DBname
else:
    def nothing(key):
        return
    enterKey = nothing
    VK_HanYoung = None
    vocaDB = "./"+DBname

def sinput(prompt):
    return input(prompt).strip()

def listing(argv):
    print("%-5s %-6s %-15s %s"%("Index", "Weight", "Word", "Meanings"))
    for n, i in enumerate(vocaList):
        print("%-5d %-6d %-15s %s"%(n+1, i[0], i[1], " ".join(i[2:])))
    print("")

def chooseRandomWord():
    minWeight = min(vocaList)[0]
    minWeightedpair = random.choice(list(filter(lambda x: x[0] == minWeight, vocaList)))
    return minWeightedpair

def noIdea(pair, WorM):
    if WorM == 1:
        print(", ".join(pair[2:]))
    else:
        print(pair[1])
    return "noIdea"

def end(*args):
    print("\n-The Practice Terminated.-\n")
    return "end"

def correct(pair, WorM):
    vocaList[vocaList.index(pair)][0]+=1
    updateVocaListFile()
    return "correct"

def incorrect(*args):
    replyIncorrect = ["No.", "Nope."]
    print(random.choice(replyIncorrect))
    return "incorrect"

def practice(argv):
    print("\nPractice Mode Start")
    print("\n**Use 'end' or 'exit' to terminate this practice mode.")
    print("**Use '?' to check the answer.\n")
    previousState = None
    prevWorM = None
    questionCharList = [":", "%", "@", "&", "-", "~", ">", "?", "/", "#", "_", "="]
    while previousState != "end":
        ansSet = { # default commands
            "end" : end, 
            "exit" : end, 
            "?" : noIdea,
            "clear" : clear
        }
        # If previous answer was incorrect or clear, then ask question again
        if not previousState in ["incorrect", "clear"]:
            wordOrMeaning = random.randint(1,2)
            pair = chooseRandomWord()
        # compose the question and answer sheet
        queSalt = ["", " ", "*"]
        if wordOrMeaning == 1: # the question is english word
            que = "%s%s%s "%(random.choice(queSalt), pair[1], random.choice(questionCharList))
            for meaning in pair[2:]:
                ansSet[meaning] = correct
        else: # the question is korean meanings
            questStr = ", ".join(pair[2:])
            if set(argv).intersection({"--easy", "-e"}):
                questStr = pair[2]
            que = "%s%s%s "%(random.choice(queSalt), questStr, random.choice(questionCharList))
            ansSet[pair[1]] = correct
        # get answer after automatic English-Korean conversion
        if prevWorM != wordOrMeaning:
            enterKey(VK_HanYoung)
        ans = sinput(que)
        # check the answer whether correct or not
        if not ans in ansSet:
            previousState = incorrect(pair, wordOrMeaning)
        else:
            result = ansSet[ans]
            if set(argv).intersection({"--easy", "-e"}) and ans == "?":
                pair = pair[:3]
            previousState = result(pair, wordOrMeaning)
        prevWorM = wordOrMeaning

def updateVocaListFile():
    with open(vocaDB, 'w', encoding='UTF-8') as vocaListFile:
        for i in vocaList:
            vocaListFile.write(("%d"+division+"%s"+division+"%s\n")%(i[0], i[1], division.join(i[2:])))

def addMeanings(argv, word):
    if set(argv).intersection({"--reference","-r"}):
        Reference.reference([word])
    pair=[0, word]
    enterKey(VK_HanYoung)
    meaning = sinput("meaning$ ")
    while not meaning in ["end", "exit", ""]:
        pair.append(meaning)
        meaning = sinput("meaning$ ")
    if len(pair) > 2:
        vocaList.append(pair)
        updateVocaListFile()

def add(argv):
    terms = argv[:]
    terms = list(filter(lambda term: term not in ["-r", "--reference"], terms))
    if terms:
        addMeanings(argv," ".join(terms))
        return
    print("\nAddition Mode Start")
    print("\n**You can submit multiple meanings for each English word.")
    print("**Automatic English-Korean conversion will be supported.")
    print("**Use 'end' or 'exit' to terminate this addition mode.")
    print("**Use 'end, 'exit' or just press the enter if you have finished submitting the meanings for each word.")
    print("**If you make a mistake to submit a word, terminate this addition mode and then use 'delete' command\n")
    word = sinput("word$ ")
    while not word in ["end", "exit"]:
        addMeanings(argv, word)
        enterKey(VK_HanYoung)        
        word = sinput("word$ ")

def quit(argv):
    if argv:
        answer = sinput("\n소혜야 정말 exit이 하고 싶어? 응/아니 :")
        if answer != "응": return None
    print("\n-Thank you for using Voca Practice.-")
    time.sleep(0.5)
    return "exit"

def delete(argv):
    if not argv:
        print("**Please enter an index what you want to delete next to the delete command.**\n")
    elif int(argv[0]) <= 0 or int(argv[0]) > len(vocaList) or not argv[0].isdigit():
        print("**There is no index, '%s'**\n"%argv[0])
    else:
        check = input("Are you sure? y/n ")
        if check == "y":
            deletedpair = vocaList.pop(int(argv[0])-1)
            updateVocaListFile()
            print("-'%s %s' was deleted.-\n"%(deletedpair[1], " ".join(deletedpair[2:])))
        else: print("Canceled\n")

def help(argv):
    explanationSet = {
        listing : "'list', 'ls' and 'l' show list of word you had submitted.\n e.g. VocaPractice$ ls",
        practice : "'practice' and 'p' start pratice mode for memorizaiton of your English words.\n e.g. VocaPractice$ p",
        add : "'add' and 'a' start addition mode for adding some words to memorize.\n e.g. VocaPractice$ a",
        quit : "'exit' terminates this program.\n e.g. VocaPractice$ exit",
        help : "'help' and 'h' show explanations of the commands.\n e.g. VocaPractice$ h p l",
        delete : "'delete' and 'd' delete the word had the index which you entered next to the command.\n e.g. VocaPractice$ d 3",
        clear : "'clear' cleans your prompt.\n e.g. VocaPractice$ clear"
    }
    print("")
    if not argv:
        for aphorism in explanationSet:
            print(explanationSet[aphorism])
    else:
        for command in argv:
            if not command in commandSet: print("**There is no command, '%s'**\n"%command)
            else: print(explanationSet[commandSet[command]])
    print("")

def clear(*args):
    os.system("clear")
    return "clear"

def restart(*args):
    if platform.system() == "Windows":
        command = "python ./VocaPractice.py"
    else:
        command = "python3 ./VocaPractice.py"
    os.system(command)
    exit()

def revise(argv):
    if set(argv).intersection({"--removeblank"}):
        reply = input("Are you sure? y/n")
        if reply == "y":
            return
        for i, pair in enumerate(vocaList):
            for j, meaning in pair[2:]:
                vocaList[i][j+2] = meaning.replace(" ", "")
        return
    if not argv or int(argv[0]) <= 0 or int(argv[0]) > len(vocaList) or not argv[0].isdigit():
        print("NO INDEX INPUT")
    else:
        print("*keep it or meanings enough: just press 'enter' key\n*delete it: write 'ㄴ'\n*else: write new meaning\n")
        enterKey(VK_HanYoung)
        idx = int(argv[0])-1
        toberevised = vocaList[idx][2:]
        meanings = toberevised[:]
        for n,meaning in enumerate(meanings):
            new = sinput(meaning+"-> ")
            if not new:
                continue
            if new != 'ㄴ':
                toberevised[n] = new
            else:
                toberevised.pop(n)
            vocaList[idx][2:] = toberevised
            updateVocaListFile()
        tobeadded = sinput("Addition?-> ")
        while not tobeadded in ["", "ㄴ"]:
            vocaList[idx].append(tobeadded)
            updateVocaListFile()
            tobeadded = sinput("Addition?-> ")
        print(vocaList[idx][1]+" was revised")
        enterKey(VK_HanYoung)

def openSrc(argv):
    conventions = {
        "this" : ".",
        "db" : "\""+vocaDB+"\""
    }
    file = " ".join(argv)
    if file in conventions:
        file = conventions[file]
    os.system("code "+ file)
    return "code"

# give a hint like a?h?ri?? for "aphorism"
def hint(argv):
    pass

# special functions
article = Articles.article
preposition = Articles.preposition
reference = Reference.reference

# list of commands
commandSet = {
    "list" : listing,
    "l" : listing,
    "ls" : listing,
    "practice" : practice, 
    "p" : practice, 
    "add" : add, 
    "a" : add, 
    "exit" : quit, 
    "help" : help,
    "h" : help,
    "delete" : delete,
    "d" : delete,
    "clear" : clear,
    "reference" : reference,
    "ref" : reference,
    "hint" : hint,
    "article" : article,
    "preposition" : preposition,
    "prep" : preposition,
    "restart" : restart,
    "revise" : revise,
    "code" : openSrc 
}
def main():
    print(
"""\nWelcome to Voca Practice.
If you need a help, submit 'help'.\n""")
    global vocaList
    vocaList = loadVocaList()
    command = ""
    while command != "exit":
        value = sinput("VocaPractice$ ")
        (command, argv) = parseInput(value) # command: string, argv: list of string
        if not command: help(argv)
        elif not command in commandSet: print("There is no command, '%s'\n"%(command))
        elif command in ["practice","p"] and not vocaList: print("***There is no words.***\nPlease use 'add' or 'a' command to add some words.\n")
        else: 
            mode = commandSet[command]
            command = mode(argv)

def loadVocaList():
    # just generate the file
    with open(vocaDB, 'a', encoding='UTF-8') as vocaListFile:
        if os.path.getsize(vocaDB) <= 0:
            return []
    with open(vocaDB, 'r', encoding='UTF-8') as vocaListFile:
        for n,i in enumerate(vocaListFile):
            pair = i.strip().split(division) # a line
            pair[0] = int(pair[0]) # weight
            vocaList.append(pair)
        return vocaList

def parseInput(value): 
    arglist = value.split()
    if not arglist:
        return ([], [])
    command = arglist[0]
    argv = arglist[1:]
    return (command, argv)

if __name__ == "__main__":
    main()
