from PasswordExtractorStrategy.DictionaryLinesExtractorStrategy import *
from Dezipper import *
from ZipExtractor import *
from PasswordMutator import *

class Main:
    def __init__(self, zippedFilePath, dictionaryFilePath):
        dictionaryLinesExtractorStrategy = DictionaryLinesExtractorStrategy(dictionaryFilePath)
        dezipper = Dezipper(zippedFilePath)
        passwordMutator = PasswordMutator()
        self.zipExtractor = ZipExtractor(dezipper, dictionaryLinesExtractorStrategy, passwordMutator)

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