
from math import *

class ProgressOutput:
    def __init__(self):
        self.lastGlobalProgressPercent = -1

    def displayProgress(self, progressionDict, nbTotalLines):
        globalProgressPercent = -1
        globalNbTestedLines = 0
        detailsToDisplay = ''

        for pid in progressionDict.keys():
            globalNbTestedLines += progressionDict[pid]['nbTestedLines']
            detailsToDisplay += ' - ' + str(progressionDict[pid]['percent']) + '%' + ' (' + str(progressionDict[pid]['nbTestedLines']) + '/' + str(progressionDict[pid]['nbTotalLinesToTest']) + ')'

        globalProgressPercent = floor(globalNbTestedLines/nbTotalLines*100)

        if (globalProgressPercent > self.lastGlobalProgressPercent):
            self.lastGlobalProgressPercent = globalProgressPercent
            print(str(globalProgressPercent) + '% ' + '(' +str(globalNbTestedLines) + '/' + str(nbTotalLines) + ')' +  '. By process:' + detailsToDisplay)