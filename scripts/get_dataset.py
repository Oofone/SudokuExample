# -*- coding: utf-8 -*-
import os
import sys
import requests

from definitions import ROOT_DIR

ADDRESS = "https://s3.ap-south-1.amazonaws.com/shreyas-gopal-personal/sudoku.csv"
FILE_NAME = "sudoku.csv"

def fetch():
    global ADDRESS, FILE_NAME

    DATA_DIR = ROOT_DIR + '/dataset/'
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)

    FILE_NAME = DATA_DIR + FILE_NAME
    if os.path.exists(FILE_NAME):
        print "Dataset already exists"
        return False

    with open(FILE_NAME, "w") as f:
        print "Downloading %s" % FILE_NAME
        response = requests.get(ADDRESS, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                sys.stdout.flush()
    return True
