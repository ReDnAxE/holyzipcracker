import itertools, sys, re
from zipfile import ZipFile

passwordMangleTabRegexs=[
    #("","","no change"), #TODO: DELETE
    ("^\w{1,5} \d{1,4}:\d{1,4} ","","del prefixes"),
    ("\.","","del points"),
    ("[^\w]+","","delete all non alphabetic characters"),
    ("FUNCTION","TOLOWERCASE","to lowercase")
]


def extract(zfile, password, description):
    #print (description + ' : ' + password)
    try:
        with ZipFile(zfile) as zf:
            zf.extractall(pwd=password.encode())
            zf.close()
        return True
    except KeyboardInterrupt:
        exit(0)
    except:
        return False


def manglePasswordAndExtract(zfile, password, passwordMangleTabRegexs):
    global re
    for regex,replacement,description in passwordMangleTabRegexs:
        if regex == 'FUNCTION': #TODO: allow multiple functions
            password = password.lower()
        else:
            password = re.sub(regex, replacement, password)

        opened = extract(zfile, password, description)

        if opened == True:
            print ('mangled password found !!! ' + password)
            return password

    return False


def printRegexsUsed(passwordMangleTabRegexs):
    for x in range(len(passwordMangleTabRegexs)):
         print (' - ' + passwordMangleTabRegexs[x][2], end='')
    print ('\n')


def generateRegexsPermutsPossibilities(indice, passwordMangleTabRegexs, nbRegexs):
    mem = ''

    if indice == nbRegexs:
        #TODO: yield avec le permutedTab
        #printRegexsUsed(passwordMangleTabRegexs)
        yield passwordMangleTabRegexs
        return

    for i in range(indice, nbRegexs):
        mem = passwordMangleTabRegexs[indice]
        passwordMangleTabRegexs[indice] = passwordMangleTabRegexs[i]
        passwordMangleTabRegexs[i] = mem

        yield from generateRegexsPermutsPossibilities(indice + 1, passwordMangleTabRegexs, nbRegexs)

        mem = passwordMangleTabRegexs[indice]
        passwordMangleTabRegexs[indice] = passwordMangleTabRegexs[i]
        passwordMangleTabRegexs[i] = mem

    return 0


def dictionary(zfile, dic):
    #TODO: check utility of back file generated
    global re
    password = ''
    try:
        f = open(back,'r')
        data = f.readline().strip()
        if 'pwd' == data[:3]:
            password = data[4:]
            return password
        else:
            start = int(data)
        f.close()
    except:
        start = 1
    dictionaryFile = open(dic,'r')
    try:
        zf = zipfile.ZipFile(zfile)
        files = zf.infolist()
        data = zf.read(files[0],pwd = password)
        zf.close()
        flag = True
    except KeyboardInterrupt:
        exit(0)
    except:
        flag = False
    if not flag:
        dlist = dictionaryFile.readlines()
        nbLines = len(dlist)
        for i in range(start,nbLines):

            percentProgress = (i / nbLines * 100)

            if (100 % percentProgress == 0):
                print (str(percentProgress) + '%')

            passwordToTest = re.sub('\n', '', dlist[i]) #default delete new lines
            try:
                #print ('\n\nNew password to mangle : ' + passwordToTest, end='')
                generatorRegexs = generateRegexsPermutsPossibilities(0, passwordMangleTabRegexs, len(passwordMangleTabRegexs))
                for generatedRegexsTab in generatorRegexs:
                    #print ('\nchange regex order and retry...')
                    passwordFounded = manglePasswordAndExtract(zfile, passwordToTest, generatedRegexsTab)
                    if passwordFounded:
                        return passwordFounded
            except KeyboardInterrupt:
                exit(0)
    print ('Password Not Found!!!')
    return


if __name__ == '__main__':
    arg = sys.argv[1:]
    if arg[1] == '-d':
        print ('Processing...')
        fl = arg[2].split('=')[1]
        password = dictionary(arg[0],fl)

        if (password):
            back = '.passwordfound.data'
            f = open(back,'w')
            f.write('pwd:' + password)
            f.close()

        exit(0)
    else:
        exit(0)