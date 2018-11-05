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
STATE = ["LCA_CASE_WORKLOC1_STATE", "STATE_1", "WORKSITE_STATE",
         "WORK_LOCATION_STATE1"]
SOC_NAME = ["LCA_CASE_SOC_NAME", "SOC_NAME", "OCCUPATIONAL_TITLE"]

COLUMN_DEFS = {"status": STATUS, "state": STATE, "soc_name": SOC_NAME}

KEY_NAME = "status"
KEY_VALUE = "CERTIFIED"

OUT_STRINGS = {"soc_name":
               "TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n",
               "state":
               "TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n"}
OUT_COUNT = 10


def extract_word(words, index):
    """return the word at the specified index after normalizing it"""
    return words[index].strip().replace("\"", "").replace("\'", "").upper()


def count_filings(inf, cols, match_name, match_val):
    """
    for every line in inf file, if the value in match_name column
    equals the match value, then the columns specified by
    the col struct are used to do counting as follows:
        extract the value in the column - it is an instance of values for the
        column. Count the number of each instance in the file and store them
        in the dictionary result. Result is a dictionary of dictionary. At
        outer level, the key is column name, at inner level, the key is
        instance of column value and value is number of
        occurances
    """

    result = {}
    col_name = []
    col_index = []

    # prepare two parallel lists - column name and column index
    # so as to avoid dictionary lookup for column index in main loop
    for c in cols:
        if c != match_name:
            col_name.append(c)
            col_index.append(cols[c])
            result[c] = {}
        else:
            match_col = cols[c]

    # main counting loop
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
    """ checks if any of alternative names for a column has a match """
    for s in pat:
        if s == word:
            return True
    return False


def find_col_indices(inf, cols, column_defs):
    """
    searches for column names in the header line in data file
    - Updates the dictionary cols with the index at which the column occurs
    - return True if all the columns were found and False otherwise after
      printing error
    """

    # initialize the cols dictionary
    for c in COLUMN_DEFS:
        cols[c] = -1

    # skip any blank lines at top
    for line in inf:
        if (line.strip()):
            break
    words = line.split(";")

    # find the index for each column
    for i, word in enumerate(words):
        word = word.upper().strip().replace("\"", "").replace("\'", "").upper()
        for key in cols:
            if (cols[key] == -1):
                if (match_col_name(word, column_defs[key]) is True):
                    cols[key] = i
                    break

    # check if indices for all the columns were found
    for t, v in cols.items():
        if (v == -1):
            print("could not find column for " + t)
            return False
    return True


def sort_by_value_and_key(indict):
    """
    by value in descending order and then by key in ascending order
    returns a new list of tuples instead of dictionary
    """
    l = [(key, val) for key, val in indict.items()]
    l.sort(key=itemgetter(0))
    l.sort(key=itemgetter(1), reverse=True)
    return l


def output_top_filings(result, total, out_strings, out_count):
    """
    Provides the writing of results to the output file corresponding
    to the current requirements
    """

    for i, c in enumerate(out_strings):
        try:
            fh = open(sys.argv[i+2], "w")
            lc = sort_by_value_and_key(result[c])
            fh.write(out_strings[c])
            for i in range(min(out_count, len(lc))):
                fh.write("{};{};{:.1%}\n".format(lc[i][0], lc[i][1],
                                                 lc[i][1]/total))
        except IOError as err:
            print("File error:{}".format(err))
        finally:
            fh.close()


def get_top_filings():
    """
    Supports the first requirement from the editor of returning a list
    of top filings by state and by name associated with occupation code
    For the inevitable new request -
        some requests (such as can you give me top 20; or filigins that were
        not certified; or the column name has changes) can be met by changing
        the constants at the top of file
        other requests such as getting the bottom states will require more
        work of adding keyword for type of request and a list of states

    The attempt is that the changes will be minimal as additional requests come
    in and should be met by adding for constant definitions to keep abstracting
    it further
    """

    # The number of columns in COLUMN_DEFS is one more than number of outfiles
    nargs = len(COLUMN_DEFS) + 1
    if len(sys.argv) != nargs:
        print("h1bcounting.py: requires exactly {} arguments".format(nargs))
        print("usage is h1bcounting.py <input_file> <outfile> ...")
        return
    # open input data file
    try:
        i = 1
        inf = open(sys.argv[i], "r")
    except IOError as err:
        print("File open error: {}".format(err))
        return

    # parse the column names to find the indices for desired columns
    cols = {}
    if (find_col_indices(inf, cols, COLUMN_DEFS) is False):
        return

    # count the filing
    result, total = count_filings(inf, cols, KEY_NAME, KEY_VALUE)
    # write out the result
    output_top_filings(result, total, OUT_STRINGS, OUT_COUNT)


def main():
    """
    only reason to have a one liner main function is to be a little
    future looking. If additional requirements are added that require
    a different processing function in addition to the current one, this
    is the place to demultiplex
    """
    get_top_filings()


if __name__ == '__main__':
    main()
