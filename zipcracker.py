import zipfile, itertools, sys, re

passwordMangleTabRegexs=[
    ("\n","","del new lines"),
    ("^\w{1,5} \d{1,4}:\d{1,4} ","","del prefixes"),
    ("\.","","del points"),
    ("[^\w]+","","delete all special characters"),
    ("FUNCTION","TOLOWERCASE","to lowercase")
]


def extract(zfile,password, description):
    print 'test: %s (%s)' %password %description
    try:
        zf = zipfile.ZipFile(zfile)
        files = zf.infolist()
        zf.read(files[0],pwd = password)
        zf.close()
        return True
    except KeyboardInterrupt:
        exit(0)
    except:
        return False


def manglePasswordAndExtract(zfile, password):
    print '\nbefore mangle: %s' %password
    global passwordMangleTabRegexs, re
    for regex,replacement,description in passwordMangleTabRegexs:
        if regex == 'FUNCTION': #TODO: allow multiple functions
            password = password.lower()
        else:
            password = re.sub(regex, replacement, password)

        print description
        flag = extract(zfile, password, description)
        if flag == True:
            print 'mangled password found !!! %s' %password
            return True

    return False


def printRegexsUsed(passwordMangleTabRegexs):
    for x in range(len(passwordMangleTabRegexs)):
         print ' - ' + passwordMangleTabRegexs[x][2],
    print '' #\n


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
    back = '.' + zfile +'.data'
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
        for i in xrange(start,len(dlist)):
            try:
                flag = generateRegexsPermutsPossibilities(0, passwordMangleTabRegexs, len(passwordMangleTabRegexs))
                #flag = manglePasswordAndExtract(zfile, dlist[i])
                if flag:
                    password = dlist[i]
                    break
            except KeyboardInterrupt:
                exit(0)
    if not flag:
        print 'Password Not Found!!!'
        exit(0)
    f = open(back,'w')
    f.write('pwd:' + password)
    f.close()
    return password


if __name__ == '__main__':
    arg = sys.argv[1:]
    if arg[1] == '-d':
        print 'Processing...'
        fl = arg[2].split('=')[1]
        #TEMP
        password = dictionary(arg[0],fl)
        #FINTEMP

        print 'Password is "%s" without quotes.' %password
    else:
        exit(0)