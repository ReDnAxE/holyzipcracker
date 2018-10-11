import datetime, os

from DictionaryLinesExtractorStrategy import *
from DictionaryCharByCharExtractorStrategy import *
from ZipExtractor import *
from Dezipper import *
from ZipExtractor import *
from PasswordMutator import *

class ZipExtractorFactory:
    def startNewZipExtractorInstance(self, zippedFilePath, dictionaryFilePath, startAtLine, endAtLine, progressionDict):
        zipExtractor = self.getZipExtractor(zippedFilePath, dictionaryFilePath, startAtLine, endAtLine)

        startDate = datetime.datetime.now()
        print (str(os.getpid()) + ' Processing (line ' + str(startAtLine) + ' to ' + str(endAtLine) + ')... ' + str(startDate))
        foundedPassword = zipExtractor.start(progressionDict)
        endDate = datetime.datetime.now()
        durationTime = endDate - startDate

        if (foundedPassword):
            print (str(os.getpid()) + ' mangled password found !!! ' + foundedPassword + ' (' + str(durationTime) + ')')
            return foundedPassword
        print (str(os.getpid()) + ' Password Not Found... (' + str(durationTime) + ')')

        return False


    def getZipExtractor(self, zippedFilePath, dictionaryFilePath, startAtLine, endAtLine):
        dezipper = Dezipper(zippedFilePath)
        #passwordExtractorStrategy = DictionaryLinesExtractorStrategy(dictionaryFilePath, startAtLine, endAtLine)
        passwordExtractorStrategy = DictionaryCharByCharExtractorStrategy(dictionaryFilePath, startAtLine, endAtLine)

        passwordMutator = PasswordMutator()
        return ZipExtractor(dezipper, passwordExtractorStrategy, passwordMutator)
