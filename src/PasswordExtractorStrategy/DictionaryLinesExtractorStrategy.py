from math import *
import re, sys, os

class DictionaryLinesExtractorStrategy: #implement PasswordExtractorStrategy
    def __init__(self, dictionaryFilePath, startAtLine = 0, endAtLine = 0):
        self.dictionaryFilePath = dictionaryFilePath
        self.dictionaryFile = open(self.dictionaryFilePath, 'r')
        self.startAtLine = startAtLine
        self.endAtLine = endAtLine
        #self.percentProgress = -1
        self.currentLine = 0

    def getPasswords(self):
        dlist = self.dictionaryFile.readlines()
        if self.endAtLine == 0:
            self.endAtLine = self.getTotal()

        #percent = -1

        for i in range(self.startAtLine, self.endAtLine):
            self.currentLine = i
            #percentProgress = floor(i / self.endAtLine * 100)

            #if (percentProgress > percent):
            #    percent = percentProgress
            #    print (str(i) + '/' + str(self.endAtLine) + ' : ' + str(percent) + '%')
            #print (str(os.getpid()) + re.sub('\n', '', dlist[i]))
            yield re.sub('\n', '', dlist[i])

    def getTotal(self):
        nbLines = sum(1 for line in open(self.dictionaryFilePath))
        return nbLines

    def getPercentProgress(self):
        return floor((self.currentLine - self.startAtLine) / (self.endAtLine - self.startAtLine) * 100)