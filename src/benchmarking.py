# -*- coding: utf-8 -*-
from utils.datasetutils import loadBatchN
from src.sudoku get getTestCase, solve

def runBatchN(n):
    df = loadBatchN(n)

    total_length = 200000
    dl = 0
    correct = 0
    netttime = 0

    for data in df.iterrows():
        sdoku, soln = getTestCase(testInstance = data["puzzle"], solution = data["solution"])
        fin, time = solve(sdoku)

        if np.array_equal(fin, soln):
            correct += 1
        nettime += time

        dl += 1
        done = int(50 * dl / total_length)
        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
        sys.stdout.flush()

    print "Accuracy: " + str((float(correct) / 200000.0) * 100) + "%"
    print "Time Taken in Minutes: " + str(float(nettime)/60.0)
