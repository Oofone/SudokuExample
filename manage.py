# -*- coding: utf-8 -*-
from src.sudoku import getTestCase, solve
from src.benchmarking import runBatchN
from scripts.get_dataset import fetch

import sys

def solveRandom():
    print "Solving a random test-case"
    arr, soln = getTestCase()
    print solve(arr, verbose = True)[0]
    print "Actual solution from dataset:"
    print soln

def main():
    operation = sys.argv[1]
    if operation.lower() == "solverandom":
        solveRandom()
    elif operation.lower() == "getdataset":
        if fetch():
            print "Dataset Successfully Retreived"
        else:
            print "Dataset Not Downloaded"
    elif operation.lower() == "trybatch":
        if len(sys.argv) < 3:
            raise Exception("Parameter 3 required. Specify batch number.")
        else:
            runBatchN(int(sys.argv[2]))

if __name__ == '__main__':
    main()
