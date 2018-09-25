from zipfile import ZipFile

class Dezipper:

    def __init__(self, zippedFilePath):
        self.zippedFilePath = zippedFilePath

    def extractZip(self, password):
        try:
            with ZipFile(self.zippedFilePath) as zipFile:
                zipFile.extractall(pwd=password.encode())
                zipFile.close()
            return True
        except KeyboardInterrupt:
            exit(0) #TODO: remplacer
        except:
            return False