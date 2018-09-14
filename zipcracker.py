import itertools, sys, re, datetime
from zipfile import ZipFile
from math import *

passwordMangleTabRegexs=[
    ("\.","","del points"),
    ("[^\w]+","","delete all non alphabetic characters"),
    ("[\d]+","","delete all numeric characters"),
    ("FUNCTION","TOLOWERCASE","to lowercase")
]


def extract(zfile, password):
    try:
        with ZipFile(zfile) as zf:
            zf.extractall(pwd=password.encode())
            zf.close()
        return True
    except KeyboardInterrupt:
        exit(0)
    except:
        return False


def getMangledPaswords(password, reorderedRegexsTab):
    global re

    for regex,replacement,description in reorderedRegexsTab:
        if regex == 'FUNCTION': #TODO: allow multiple functions
            password = password.lower()
        else:
            password = re.sub(regex, replacement, password)

        yield password


def printRegexsUsed(passwordMangleTabRegexs):
    for x in range(len(passwordMangleTabRegexs)):
         print (' - ' + passwordMangleTabRegexs[x][2], end='')
    print ('\n')


def generateRegexsPermutsPossibilities(indice, passwordMangleTabRegexs, nbRegexs):
    mem = ''

    if indice == nbRegexs:
        #TODO: yield avec le permutedTab
        #printRegexsUsed(passwordMangleTabRegexs)
        yield passwordMangleTabRegexs
        return

    for i in range(indice, nbRegexs):
        mem = passwordMangleTabRegexs[indice]
        passwordMangleTabRegexs[indice] = passwordMangleTabRegexs[i]
        passwordMangleTabRegexs[i] = mem

        yield from generateRegexsPermutsPossibilities(indice + 1, passwordMangleTabRegexs, nbRegexs)

        mem = passwordMangleTabRegexs[indice]
        passwordMangleTabRegexs[indice] = passwordMangleTabRegexs[i]
        passwordMangleTabRegexs[i] = mem

    return 0


def getPasswordsToTestFromDictionary(dictionaryFile, startAt):
    dlist = dictionaryFile.readlines()
    nbLines = len(dlist)
    percent = -1
    start = startAt

    for i in range(startAt,nbLines):
        percentProgress = floor(i / nbLines * 100)
        if (percentProgress > percent):
            percent = percentProgress
            print (str(i) + '/' + str(nbLines) + ' : ' + str(percent) + '%')

        passwordToTest = re.sub('\n', '', dlist[i])
        passwordToTest = passwordToTest.rstrip()
        passwordToTest = passwordToTest.lstrip()
        #OR PERHAPS = passwordToTest.strip(' \t\n\r')

        yield passwordToTest

        for reorderedRegexsTab in generateRegexsPermutsPossibilities(0, passwordMangleTabRegexs, len(passwordMangleTabRegexs)):
            for mangledPasswordToTest in getMangledPaswords(passwordToTest, reorderedRegexsTab):
                yield mangledPasswordToTest


def dictionaryStrategy(zfile, dic):
    #TODO: check utility of back file generated
    global re
    password = ''
    startDate = now = datetime.datetime.now()

    print ('Processing dictionary strategy... ' + str(startDate))

    try:
        f = open(back,'r')
        data = f.readline().strip()
        if 'pwd' == data[:3]:
            password = data[4:]
            return password
        else:
            startAt = int(data)
        f.close()
    except:
        startAt = 1
    dictionaryFile = open(dic,'r')
    try:
        zf = zipfile.ZipFile(zfile)
        files = zf.infolist()
        data = zf.read(files[0],pwd = password)
        zf.close()
        flag = True
    except KeyboardInterrupt:
        exit(0)
    except:
        flag = False
    if not flag:
        for passwordToTest in getPasswordsToTestFromDictionary(dictionaryFile, startAt):
            try:
                if extract(zfile, passwordToTest):
                    print ('mangled password found !!! ' + passwordToTest)
                    return passwordToTest
            except KeyboardInterrupt:
                exit(0)
    print ('Password Not Found... ' + str(datetime.datetime.now()))
    return


if __name__ == '__main__':
    arg = sys.argv[1:]
    if arg[1] == '-d':
        fl = arg[2].split('=')[1]
        passwordFounded = dictionaryStrategy(arg[0],fl)

        if (passwordFounded):
            back = '.passwordfound.data'
            f = open(back,'w')
            f.write('pwd:' + passwordFounded)
            f.close()

        exit(0)
    else:
        exit(0)