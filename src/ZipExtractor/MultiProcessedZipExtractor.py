import datetime, os
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

        for i in range(self.nbProcesses):
            p = mp.Process(target=self.process, args=(self.zippedFilePath, self.dictionaryFilePath, chunkedLinesNumbers[i][0], chunkedLinesNumbers[i][1]))
            self.processes.append(p)

        [x.start() for x in self.processes]

    def process(self, zippedFilePath, dictionaryFilePath, startAtLine, endAtLine):
        self.zipExtractorFactory.startNewZipExtractorInstance(zippedFilePath, dictionaryFilePath, startAtLine, endAtLine)

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
