import datetime, os, time
from math import *
import multiprocessing as mp

from DictionaryLinesExtractorStrategy import *
from ZipExtractorFactory import *
from Dezipper import *
from PasswordMutator import *
from ProgressOutput import *

class MultiProcessedZipExtractor:
    def __init__(self, zippedFilePath, dictionaryFilePath):
        self.zippedFilePath = zippedFilePath
        self.dictionaryFilePath = dictionaryFilePath
        self.processes = []
        self.nbProcesses = mp.cpu_count()
        self.zipExtractorFactory = ZipExtractorFactory()
        self.progressOutput = ProgressOutput()
        self.nbTotalLines = 0
        #TODO: test multiprocessing contexts and start methods (spawn, fork, forkserver)
        mp.set_start_method('fork')
        self.mpManager = mp.Manager()


    def start(self):
        chunkedLinesNumbers = self.getChunkedLinesNumbers()
        passwordFoundEvent = self.mpManager.Event()
        progressionDict = self.mpManager.dict()

        for i in range(self.nbProcesses):
            p = mp.Process(target=self.process, args=(self.zippedFilePath, self.dictionaryFilePath, chunkedLinesNumbers[i][0], chunkedLinesNumbers[i][1], passwordFoundEvent, progressionDict))
            self.processes.append(p)

        [process.start() for process in self.processes]
        self.watchProcesses(passwordFoundEvent, progressionDict)


    def watchProcesses(self, passwordFoundEvent, progressionDict):
        while True:
            if (any(process.is_alive() for process in self.processes)):
                if (passwordFoundEvent.is_set() is True):
                    [process.kill() for process in self.processes]
                else:
                    time.sleep(1)
                    self.progressOutput.displayProgress(progressionDict, self.nbTotalLines)
            else:
                break


    def process(self, zippedFilePath, dictionaryFilePath, startAtLine, endAtLine, passwordFoundEvent, progressionDict):
        foundedPassword = self.zipExtractorFactory.startNewZipExtractorInstance(zippedFilePath, dictionaryFilePath, startAtLine, endAtLine, progressionDict)
        if (foundedPassword):
            passwordFoundEvent.set()

#TODO: debug 0 à 1, 1 à 2, 2 à 3. >>> 0 à 0, 0 à 1
    def getChunkedLinesNumbers(self):
        dictionaryLinesExtractorStrategy = DictionaryLinesExtractorStrategy(self.dictionaryFilePath)
        self.nbTotalLines = dictionaryLinesExtractorStrategy.getTotal()

        chunkedLinesNumbers = []
        partNbLines = floor(self.nbTotalLines / self.nbProcesses)
        rest = self.nbTotalLines % self.nbProcesses

        startAtLine = 0
        endAtLine = partNbLines

        for i in range(self.nbProcesses):
            chunkedLinesNumbers.append([startAtLine, endAtLine])
            startAtLine += partNbLines
            endAtLine = startAtLine + partNbLines

        chunkedLinesNumbers[-1][1] = chunkedLinesNumbers[-1][1] + rest

        return chunkedLinesNumbers
