import datetime, hashlib

class ZipExtractor:
    def __init__(self, dezipper, passwordExtractorStrategy, passwordMutator):
        self.dezipper = dezipper
        self.passwordExtractorStrategy = passwordExtractorStrategy
        self.passwordMutator = passwordMutator


    def start(self):
        for passwordToTest in self.getPasswords():
            if self.dezipper.extractZip(passwordToTest):
                return passwordToTest
        return False


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

    #def getProgress(self):
    #    