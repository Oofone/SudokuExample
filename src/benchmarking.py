# -*- coding: utf-8 -*-
from utils.datasetutils import loadBatchN, BATCH_SIZE
from src.sudoku import getTestCase, solve

import numpy as np
import sys

def runBatchN(n):
    df = loadBatchN(n)

    total_length = BATCH_SIZE
    dl = 0
    correct = 0
    nettime = 0

    for index, data in df.iterrows():
        sdoku, soln = getTestCase(testInstance = data["puzzle"], solution = data["solution"])

        try:
            (fin, time) = solve(sdoku)
        except Exception as e:
            pass

        if (fin - soln == 0).all():
            correct += 1
        nettime += time

        dl += 1
        done = int(50 * dl / total_length)
        sys.stdout.write("\r[%s%s] \t[%s]" % ('=' * done, ' ' * (50-done) , (str(dl) + " completed of " + str(BATCH_SIZE) + " examples")))
        sys.stdout.flush()

    print "\nAccuracy: " + str((float(correct) / BATCH_SIZE) * 100) + "%"
    print "Time Taken in Minutes: " + str(float(nettime)/60.0)
