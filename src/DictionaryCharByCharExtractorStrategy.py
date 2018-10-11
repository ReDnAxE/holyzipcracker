from math import *
import re, sys, os

class DictionaryCharByCharExtractorStrategy: #implement PasswordExtractorStrategy
    def __init__(self, dictionaryFilePath, startAtLine = 0, endAtLine = 0, minPasswordLen = 10, maxPasswordLen = 50):
        self.dictionaryFilePath = dictionaryFilePath
        self.dictionaryFile = open(self.dictionaryFilePath, 'r')
        self.startAtLine = startAtLine
        self.endAtLine = endAtLine
        if self.endAtLine == 0:
            self.endAtLine = self.getTotal()
        self.currentLine = 0
        self.minPasswordLen = minPasswordLen
        self.maxPasswordLen = maxPasswordLen

    def getPasswords(self):
        for password in self.getMinToMaxPasswordsLen():
            #print(password)
            yield password

    def getMinToMaxPasswordsLen(self):
        for linesWithEnouthChar in self.getLinesWithEnouthChar():
            baseLine = linesWithEnouthChar.split('\n')[0]
            linesWithEnouthChar = re.sub('\n', ' ', linesWithEnouthChar)
            for firstCharIndex in range(0, len(baseLine) - 1):
                if (baseLine[firstCharIndex] == ' '):
                    continue
                subString = ''
                subStringLen = 0
                for char in linesWithEnouthChar[firstCharIndex:]:
                    subString += char
                    if (char != ' '):
                        subStringLen += 1
                    if (subStringLen >= self.minPasswordLen):
                        yield subString
                    if (subStringLen >= self.maxPasswordLen):
                        break

    def getLinesWithEnouthChar(self):
        dlist = self.dictionaryFile.readlines()
        for i in range(self.startAtLine, self.endAtLine):
            linesWithEnouthChar = ''
            linesWithEnouthCharLen = 0
            tmpLineIndex = i
            self.currentLine = i
            linesWithEnouthChar += dlist[i]
            while (len(re.sub(' ', '', linesWithEnouthChar)) < len(re.sub(' ', '', dlist[i])) + self.maxPasswordLen):
                try:
                    tmpLineIndex += 1
                    linesWithEnouthChar +=  dlist[tmpLineIndex]
                except (IndexError):
                    break
            yield linesWithEnouthChar

    def getTotal(self):
        nbLines = sum(1 for line in open(self.dictionaryFilePath))
        return nbLines

    def getProgress(self):
        progress = {'percent': 0, 'currentLine': self.currentLine, 'startAtLine': self.startAtLine, 'endAtLine': self.endAtLine, 'nbTestedLines': self.currentLine - self.startAtLine, 'nbTotalLinesToTest': self.endAtLine - self.startAtLine}
        progress['percent'] = floor(progress['nbTestedLines'] / progress['nbTotalLinesToTest'] * 100)

        return progress