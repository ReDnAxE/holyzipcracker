from math import *
import re, sys, os

class DictionaryLinesExtractorStrategy: #implement PasswordExtractorStrategy
    def __init__(self, dictionaryFilePath, startAtLine = 0, endAtLine = 0):
        self.dictionaryFilePath = dictionaryFilePath
        self.dictionaryFile = open(self.dictionaryFilePath, 'r')
        self.startAtLine = startAtLine
        self.endAtLine = endAtLine
        self.currentLine = 0

    def getPasswords(self):
        dlist = self.dictionaryFile.readlines()
        if self.endAtLine == 0:
            self.endAtLine = self.getTotal()
        for i in range(self.startAtLine, self.endAtLine):
            self.currentLine = i
            yield re.sub('\n', '', dlist[i])

    def getTotal(self):
        nbLines = sum(1 for line in open(self.dictionaryFilePath))
        return nbLines

    def getProgress(self):
        progress = {'percent': 0, 'currentLine': self.currentLine, 'startAtLine': self.startAtLine, 'endAtLine': self.endAtLine, 'nbTestedLines': self.currentLine - self.startAtLine, 'nbTotalLinesToTest': self.endAtLine - self.startAtLine}
        progress['percent'] = floor(progress['nbTestedLines'] / progress['nbTotalLinesToTest'] * 100)

        return progress