import datetime, os

from PasswordExtractorStrategy.DictionaryLinesExtractorStrategy import *
from ZipExtractor import *
from Dezipper import *
from ZipExtractor.ZipExtractor import *
from PasswordMutator import *

class ZipExtractorFactory:
    def startNewZipExtractorInstance(self, zippedFilePath, dictionaryFilePath, startAtLine, endAtLine):
        dezipper = Dezipper(zippedFilePath)
        dictionaryLinesExtractorStrategy = DictionaryLinesExtractorStrategy(dictionaryFilePath, startAtLine, endAtLine)
        passwordMutator = PasswordMutator()
        zipExtractor = ZipExtractor(dezipper, dictionaryLinesExtractorStrategy, passwordMutator)

        startDate = datetime.datetime.now()
        print (str(os.getpid()) + ' Processing (line ' + str(startAtLine) + ' to ' + str(endAtLine) + ')... ' + str(startDate))
        foundedPassword = zipExtractor.start()
        endDate = datetime.datetime.now()
        durationTime = endDate - startDate

        if (foundedPassword):
            print (str(os.getpid()) + ' mangled password found !!! ' + foundedPassword + ' (' + str(durationTime) + ')')
            return
        print (str(os.getpid()) + ' Password Not Found... (' + str(durationTime) + ')')