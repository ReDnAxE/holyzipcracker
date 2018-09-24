from PasswordExtractorStrategy.DictionaryLinesExtractorStrategy import *
from Dezipper import *
from ZipExtractor.MultiProcessedZipExtractor import *
from ZipExtractor.ZipExtractorFactory import *
from PasswordMutator import *

class Main:
    def __init__(self, zippedFilePath, dictionaryFilePath):
        self.zippedFilePath = zippedFilePath
        self.dictionaryFilePath = dictionaryFilePath

    def start(self):
        zipExtractorFactory = ZipExtractorFactory()
        zipExtractorFactory.startNewZipExtractorInstance(self.zippedFilePath, self.dictionaryFilePath, 0, 0)
    
    def startWithMultiProcesses(self):
        multiProcessedZipExtractor = MultiProcessedZipExtractor(self.zippedFilePath, self.dictionaryFilePath)
        multiProcessedZipExtractor.start()


        #if (passwordFounded):
        #    back = '.passwordfound.data'
        #    f = open(back,'w')
        #    f.write('pwd:' + passwordFounded)
        #    f.close()


#SCRIPT START
if __name__ == '__main__':
    args = sys.argv[1:]
    main = Main(args[0], args[1])
    #main.start()
    main.startWithMultiProcesses()