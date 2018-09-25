import datetime, os, time
from math import *
import multiprocessing as mp

from PasswordExtractorStrategy.DictionaryLinesExtractorStrategy import *
from ZipExtractor.ZipExtractorFactory import *
from Dezipper import *
from ZipExtractor.ZipExtractor import *
from PasswordMutator import *

class MultiProcessedZipExtractor:
    def __init__(self, zippedFilePath, dictionaryFilePath):
        self.zippedFilePath = zippedFilePath
        self.dictionaryFilePath = dictionaryFilePath
        self.processes = []
        self.nbProcesses = mp.cpu_count()
        self.zipExtractorFactory = ZipExtractorFactory()


    def start(self):
        chunkedLinesNumbers = self.getChunkedLinesNumbers()
        passwordFoundEvent = mp.Event()

        for i in range(self.nbProcesses):
            p = mp.Process(target=self.process, args=(self.zippedFilePath, self.dictionaryFilePath, chunkedLinesNumbers[i][0], chunkedLinesNumbers[i][1], passwordFoundEvent))
            self.processes.append(p)

        [process.start() for process in self.processes]
        self.watchProcesses(passwordFoundEvent)


    def watchProcesses(self, passwordFoundEvent):
        while True:
            if (any(process.is_alive() for process in self.processes)):
                if (passwordFoundEvent.is_set() is True):
                    [process.kill() for process in self.processes]
                else:
                    time.sleep(1)
            else:
                break


    def process(self, zippedFilePath, dictionaryFilePath, startAtLine, endAtLine, passwordFoundEvent):
        foundedPassword = self.zipExtractorFactory.startNewZipExtractorInstance(zippedFilePath, dictionaryFilePath, startAtLine, endAtLine)
        if (foundedPassword):
            passwordFoundEvent.set()


    def getChunkedLinesNumbers(self):
        dictionaryLinesExtractorStrategy = DictionaryLinesExtractorStrategy(self.dictionaryFilePath)
        nbLines = dictionaryLinesExtractorStrategy.getTotal()

        chunkedLinesNumbers = []
        partNbLines = floor(nbLines / self.nbProcesses)
        rest = nbLines % self.nbProcesses

        startAtLine = 0
        endAtLine = partNbLines

        for i in range(self.nbProcesses):
            chunkedLinesNumbers.append([startAtLine, endAtLine])
            startAtLine += partNbLines
            endAtLine = startAtLine + partNbLines

        chunkedLinesNumbers[-1][1] = chunkedLinesNumbers[-1][1] + rest

        return chunkedLinesNumbers
