from DictionaryExtractorStrategy import *
from Dezipper import *
from ZipExtractor import *

class Main:
    def __init__(self, zippedFilePath, dictionaryFilePath):
        dictionaryExtractorStrategy = DictionaryExtractorStrategy(dictionaryFilePath)
        dezipper = Dezipper(zippedFilePath)
        self.zipExtractor = ZipExtractor(dezipper, dictionaryExtractorStrategy)
    
    def start(self):
        self.zipExtractor.start()


        #if (passwordFounded):
        #    back = '.passwordfound.data'
        #    f = open(back,'w')
        #    f.write('pwd:' + passwordFounded)
        #    f.close()


#SCRIPT START
args = sys.argv[1:]
main = Main(args[0], args[1])
main.start()