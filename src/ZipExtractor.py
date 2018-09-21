import datetime, hashlib
from PasswordMutator import *

class ZipExtractor:
    def __init__(self, dezipper, passwordExtractorStrategy):
        self.dezipper = dezipper
        self.passwordExtractorStrategy = passwordExtractorStrategy
        self.passwordMutator = PasswordMutator()


    def start(self):
        startDate = datetime.datetime.now()
        print ('Processing... ' + str(startDate))

        for passwordToTest in self.getPasswords():
            try:
                if self.dezipper.extractZip(passwordToTest):
                    print ('mangled password found !!! ' + passwordToTest)
                    exit(0)
            except KeyboardInterrupt:
                exit(0)

        print ('Password Not Found... ' + str(datetime.datetime.now()))
        exit(0)


    def getPasswords(self):
        for passwordToTest in self.passwordExtractorStrategy.getPasswords():
            passwordsTestedHashes = []
            passwordToTest = passwordToTest.strip(' \t\n\r')

            yield passwordToTest
            passwordsTestedHashes.append(hashlib.sha1(passwordToTest.encode()))

            for mutatedPasswordToTest in self.passwordMutator.getMutatedPasswords(passwordToTest):
                sha1Password = hashlib.sha1(mutatedPasswordToTest.encode())
                if sha1Password.hexdigest() not in passwordsTestedHashes:
                    yield mutatedPasswordToTest
                    passwordsTestedHashes.append(hashlib.sha1(mutatedPasswordToTest.encode()))