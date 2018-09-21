import re

class PasswordMutator:
    def __init__(self):
        self.passwordMangleTabRegexs=[
            ("\.","","del points"),
            ("[^\w]+","","delete all non alphabetic characters"),
            ("[\d]+","","delete all numeric characters"),
            ("FUNCTION","TOLOWERCASE","to lowercase")
        ]


    def getMutatedPasswords(self, password):
        for reorderedRegexsTab in self.generateRegexsPermutsPossibilities(0, self.passwordMangleTabRegexs, len(self.passwordMangleTabRegexs)):
            for mangledPassword in self.getMangledPaswords(password, reorderedRegexsTab):
                yield mangledPassword


    def generateRegexsPermutsPossibilities(self, indice, passwordMangleTabRegexs, nbRegexs):
        mem = ''

        if indice == nbRegexs:
            yield passwordMangleTabRegexs
            return

        for i in range(indice, nbRegexs):
            mem = passwordMangleTabRegexs[indice]
            passwordMangleTabRegexs[indice] = passwordMangleTabRegexs[i]
            passwordMangleTabRegexs[i] = mem

            yield from self.generateRegexsPermutsPossibilities(indice + 1, passwordMangleTabRegexs, nbRegexs)

            mem = passwordMangleTabRegexs[indice]
            passwordMangleTabRegexs[indice] = passwordMangleTabRegexs[i]
            passwordMangleTabRegexs[i] = mem

        return 0


    def getMangledPaswords(self, password, reorderedRegexsTab):
        global re

        for regex,replacement,description in reorderedRegexsTab:
            if regex == 'FUNCTION': #TODO: allow multiple functions
                password = password.lower()
            else:
                password = re.sub(regex, replacement, password)

            yield password

    
    def printRegexsUsed(passwordMangleTabRegexs):
        for x in range(len(passwordMangleTabRegexs)):
            print (' - ' + passwordMangleTabRegexs[x][2], end='')
        print ('\n')