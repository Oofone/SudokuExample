# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from utils.datasetutils import getRandomCase

import sys
import numpy as np
import time

boxmap = {0:0,1:0,2:0,3:1,4:1,5:1,6:2,7:2,8:2}

def getTestCase(testInstance = None, solution = None):
    if not (testInstance or solution):
        testInstance, solution = getRandomCase()

    assert len(testInstance) == 9*9
    assert len(solution) == 9*9

    sudoku = list(testInstance)
    soln = list(solution)

    sudoku = np.array(sudoku, np.int)
    soln = np.array(soln, np.int)

    sudoku = sudoku.reshape((9,9))
    soln = soln.reshape((9,9))

    return sudoku, soln

def sumToN(n):
    return (n * (n + 1)) / 2

def getPartialSolved(arr):
    partial = (arr != 0)
    return partial

def checkDone(arr):
    blocksum = convolveWithOneSum(arr)
    checkAgainst = sumToN(9)
    if (blocksum == sumToN(9)).all() and (arr.sum(axis=0) == checkAgainst).all() and (arr.sum(axis=1) == checkAgainst).all():
        return True
    if (blocksum > sumToN(9)).any() and (arr.sum(axis=0) > checkAgainst).any() and (arr.sum(axis=1) > checkAgainst).any():
        raise Exception("The sudoku was solve incorrectly")
    else:
        return False

def convolveWithOneSum(arr):
    filter = np.zeros((3,3), np.int)
    for i in range(0,7,3):
        for j in range(0,7,3):
            roc = arr[i:i+3,j:j+3]
            filter[i/3,j/3] = np.sum(roc)
    return filter.flatten()

def getPossibilities(arr):
    inds = []
    for i in range(1,10):
        temp = np.ones(arr.shape, np.bool)
        temp[arr == i] = False
        hits = np.argwhere(temp == False)
        for points in hits:
            temp[points[0],:] = np.zeros(temp[points[0],:].shape, np.bool)
            temp[:,points[1]] = np.zeros(temp[:,points[1]].shape, np.bool)
            xstart = boxmap[points[0]]
            ystart = boxmap[points[1]]
            temp[xstart*3:xstart*3+3,ystart*3:ystart*3+3] = np.zeros((3,3), np.bool)
        temp[arr != 0] = False
        inds.append(temp)
    return np.array(inds)

def getSolvableBoxes(arr):
    arr = np.reshape(arr, (3,3))
    return np.argwhere(arr == 1)

def isSolvableInBox(tup, solvableBoxes):
    piece = np.array([boxmap[tup[0]], boxmap[tup[1]]])
    if (solvableBoxes == piece).all(1).any() :
        return True
    else:
        return False

def singleRound(array, verbose = False):
    arr = array.copy()
    start = time.time()
    possibilites = getPossibilities(arr)
    if verbose:
        print "Induvidual number possibilities:"
        print possibilites

    no = 0
    for current in possibilites:
        no += 1
        solvableBoxes = getSolvableBoxes(convolveWithOneSum(current))
        if verbose:
            print "Number " + str(no)
            print "Induvidual number possibilities:"
            print possibilites
        possibs = np.argwhere(current == True)
        for point in possibs:
            if isSolvableInBox(point, solvableBoxes):
                if verbose:
                    print "Solving for position " + str(point)
                arr[tuple(point)] = no
    end = time.time()
    return (arr, (end - start))

def solve(array, verbose = False):
    round = 1
    nettime = 0
    arr = array.copy()

    while True:
        if verbose:
            print "Starting round " + str(round)

        if checkDone(arr):
            if verbose:
                print "Solved in " + str(round - 1) + " rounds"
            break

        if round >100:
            if verbose:
                print "Unfortunately this puzzle could not be solved, returning partially solved array"
            return arr

        if verbose:
            print "Sudoku not yet solved"
            print "Performing round operations"

        arr, timeTaken = singleRound(arr)

        if verbose:
            print "Round " + str(round) + " ended in " + str(timeTaken) + " seconds"

        nettime += timeTaken
        round += 1

    if verbose:
        print "Total time taken: " + str(nettime) + " seconds"

    return (arr, nettime)
