# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 16:33:26 2018

@author: Somesh Gupta
"""
import sys
from operator import itemgetter

"""
The constants below are used to customize the application of the code and
can be modified if needed as follow:
    COLUMN_DEFS - determines what columns will be extracted from the tables.
                  It names a column and associates every column with a list of
                  strings.
                  If new columns are to be extracted, the dictionary can be
                    expanded
                  If the column is named by a new string in some year, then
                    the list of strings for that column can be expanded
    KEY_NAME and KEY_VALUE - the column and its values used to extract records
    OUT_STRINGS - these should be in the same order as the output files in
                  command line. Indicates the columns for the file and
                  header string
    OUT_COUNT - the number of top summarizations to be output
"""

STATUS = ["CASE_STATUS", "STATUS", "APPROVAL_STATUS"]
STATE = ["LCA_CASE_WORKLOC1_STATE", "WORKSITE_STATE", "STATE_1"]
SOC_NAME = ["LCA_CASE_SOC_NAME", "SOC_NAME", "OCCUPATION_TITLE"]

COLUMN_DEFS = {"status": STATUS, "state": STATE, "soc_name": SOC_NAME}

KEY_NAME = "status"
KEY_VALUE = "CERTIFIED"

OUT_STRINGS = {"soc_name":
               "TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n",
               "state":
               "TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n"}
OUT_COUNT = 10


def extract_word(words, index):
    # extract the word from list at the specified index.
    # clean it as needed
    return words[index].strip().replace("\"", "").replace("\'", "").upper()


def count_filings(inf, cols, match_name, match_val):
    # for every line in inf file, if the value in match_name column
    # equals the match value, then the columns specified by
    # the col struct are used to do counting as follows:
    #      extract the value in the column - it is an instance of values
    #      for the column. Count the number of each instance in the file
    #      and store them in the dictionary result. Result is a dictionary
    #      of dictionary. At outer level, the key is column name, at inner
    #      level, the key is instance of column value and value is number of
    #      occurances

    result = {}
    col_name = []
    col_index = []

    # prepare two parallel lists - column name and column index
    # to avoid dictionary lookup for column index in per file line loop
    for c in cols:
        print(c)
        if c != match_name:
            col_name.append(c)
            col_index.append(cols[c])
            result[c] = {}
        else:
            match_col = cols[c]

    total = 0

    for line in inf:
        words = line.strip().split(';')
        if match_val == extract_word(words, match_col):
            total += 1
            for i, n in enumerate(col_index):
                s = extract_word(words, n)
                k = col_name[i]
                result[k][s] = result[k].get(s, 0) + 1
    return result, total


def match_col_name(word, pat):
    # checks if any of alternative names for a column has a match
    for s in pat:
        if s == word:
            return True
    return False


def find_col_indices(words, cols, column_defs):
    # searches for column names in the list of words - common name is
    # in dict cols, the acceptable strings for a column name are in
    # column_defs. Returns the indices at which the names occur in cols
    for i, word in enumerate(words):
        word = word.upper()
        for key in cols:
            if (cols[key] == -1):
                if (match_col_name(word, column_defs[key]) is True):
                    cols[key] = i
                    break
    for t, v in cols.items():
        if (v == -1):
            print("could not find column for " + t)
            return False
    return True


def sort_by_value_and_key(indict):
    # first sort by value in descending order and then by key in
    # ascending order. Returns a list of tuples of key-values in sorted order
    l = [(key, val) for key, val in indict.items()]
    l.sort(key=itemgetter(0))
    l.sort(key=itemgetter(1), reverse=True)
    return l


def get_top_filings():
    nargs = len(COLUMN_DEFS) + 1
    if len(sys.argv) != num_out_files+2:
        print("h1bcounting.py: requires exactly {} arguments".format(nargs))
        print("usage is h1bcounting.py <input_file> <outfile> ...")
        return
    try:
        i = 1
        inf = open(sys.argv[i], "r")
    except IOError as err:
        print("File open error: {}".format(err))
        return

    # create a dictionary with the required column names as keys
    # initialized to a value of 1
    cols = {}
    for c in COLUMN_DEFS:
        cols[c] = -1

    # skip any blank lines at top
    for line in inf:
        if (line.strip()):
            break
    words = line.split(";")

    # parse the column names to find the indices for desired columns
    if (find_col_indices(words, cols, COLUMN_DEFS) is False):
        return

    # count the filing
    result, total = count_filings(inf, cols, KEY_NAME, KEY_VALUE)

    # from here it is not that much data driven because the output format
    # is very specific. Can be made data driven once more requirements come in

    for i, c in enumerate(OUT_STRINGS):
        try:
            fh = open(sys.argv[i+2], "w")
            lc = sort_by_value_and_key(result[c])
            fh.write(OUT_STRINGS[c])
            for i in range(min(OUT_COUNT, len(lc))):
                fh.write("{};{};{:.1%}\n".format(lc[i][0], lc[i][1],
                                                 lc[i][1]/total))
        except IOError as err:
            print("File error:{}".format(err))
        finally:
            fh.close()


def main():

    get_top_filings()


if __name__ == '__main__':
    main()
