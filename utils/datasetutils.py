import pandas as pd
import random

from definitions import ROOT_DIR

def getRandomCase():
    row = random.randint(1, 1000000)
    df = pd.read_csv(ROOT_DIR+"/dataset/sudoku.csv", skiprows=row-1, nrows=1, names=['puzzle','solution'])
    return tuple(df.iloc[0])

def loadBatchN(n):
    df = pd.read_csv(ROOT_DIR+"/dataset/sudoku.csv", skiprows=(n*200000) - 1, nrows=200000, names=['puzzle','solution'])
    return df
