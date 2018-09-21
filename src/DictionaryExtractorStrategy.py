from math import *
import re, sys

class DictionaryExtractorStrategy: #implement PasswordExtractorStrategy
    def __init__(self, dictionaryFilePath):
        self.dictionaryFile = open(dictionaryFilePath, 'r')
        self.startAt = 0

    def getPasswords(self):
        dlist = self.dictionaryFile.readlines()
        nbLines = len(dlist)
        percent = -1

        for i in range(self.startAt, nbLines):
            percentProgress = floor(i / nbLines * 100)

            if (percentProgress > percent):
                percent = percentProgress
                print (str(i) + '/' + str(nbLines) + ' : ' + str(percent) + '%')

            yield re.sub('\n', '', dlist[i])

    #TODO: récupérer pas par ligne mais par fenetres de charactères en avancant