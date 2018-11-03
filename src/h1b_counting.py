# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 16:33:26 2018

@author: Somesh Gupta
"""
import sys, os
from operator import itemgetter

def read_data(fname, fields):
    """
    Reads data from file fname. Keeps only the columns specified in the
    fields list and also accumulates data . Assumes data in the columns is numeric. 
    
    Arguments:
        fname: the file name to be used. Can be absolute or relative
        fields: list of column names to be 
    """
def extract_word(words, offset):
    #clean comment --- extracts the word at offset, cleans it and
    #returns upper case"
    return words[offset].strip().replace("\"","").replace("\'","").upper()

def count_applications(inf, cols):
    
    states = {}
    occs = {}  
    occnames = {}
    
    state_col = cols['state']
    occ_col = cols['occ_code']
    status_col = cols['status']
    occ_name_col = cols['occ_name']
    total = 0
    for line in inf:
        #print(line)
        words = line.strip().split(';')
        status = extract_word(words, status_col)
        state = extract_word(words, state_col)
        occ_code = extract_word(words, occ_col)
        occ_name = extract_word(words, occ_name_col)
        if status == 'CERTIFIED':
            total += 1
            states[state] = states.get(state, 0) + 1
            if occ_code not in occs:
                occnames[occ_code] = occ_name
                count = 1
            else:
                count = 1 + occs[occ_code]
            occs[occ_code] = count
    
    return states, occs, occnames, total

def main():


    """    
    s = f.readline()
    i = int(s.strip())
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
    """
    print(os.getcwd())
    if len(sys.argv) != 4:
        print("h1bcounting.py: requires exactly 3 arguments")
        print("usage is h1bcounting.py <input_file> <outfile_occupations> <outfile_states>")
        return

    try:
        i = 1
        inf = open(sys.argv[i], "r")
        i += 1
        foccs = open(sys.argv[i], "w")
        i += 1
        fstates = open(sys.argv[i], "w")
    except IOError as err:
        print("File open error: {}".format(err))
        return
    STATUS1 = "approval_status"
    STATUS2 = "case_status"
    STATE1 = "1_state"
    STATE2 = "state_1"
    STATE3 = "worksite_state"
    CODE1 = "occ"
    CODE2 = "soc"
    CODE3 = "code"
    NAME1 = "name"
    # Locate the columns to use
    cols = {'status':-1, 'state':-1, 'occ_code':-1, 'occ_name':-1}

    for line in inf:
        if (line.strip()):
            break;
            
    words = line.split(";")
    for i, word in enumerate(words):
        lword = word.lower()
        if cols['status'] == -1:
            if (STATUS1 in lword) or (STATUS2 in lword):
                print("found status in column  " + str(i))
                cols['status'] = i

        if cols['state'] == -1:
            if (STATE1 in lword) or (STATE2 in lword) or (STATE3 in lword):
                print("found state in column  " + str(i))
                cols['state'] = i
                    
        if cols['occ_code'] == -1:
            if (CODE1 in lword or CODE2 in lword) and (CODE3 in lword):
                print("found code in column  " + str(i))
                cols['occ_code'] = i
            
        if cols['occ_name'] == -1:
            if (CODE1 in lword or CODE2 in lword) and (NAME1 in lword):
                print("found name in column  " + str(i))
                cols['occ_name'] = i

    for t, v in cols.items():
        if (v == -1):
            print("could not find column for "+ t)
            return

    states, occs, occnames, total = count_applications(inf, cols)
    print(states)
    #print(occnames)
    #print(occs)
    
    statelist = [(key, val) for key, val in states.items()]
    statelist.sort(key = itemgetter(0))
    statelist.sort(key=itemgetter(1), reverse=True)
    
    occlist = [(key, val) for key, val in occs.items()]
    occlist.sort(key = itemgetter(0))
    occlist.sort(key=itemgetter(1), reverse=True)
    
    print(len(statelist))
    print("TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE")
    for i in range(min(10, len(statelist))):
        print("{};{};{:.1%}".format(statelist[i][0], statelist[i][1], statelist[i][1]/total))
    
    print("TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE")
    for i in range(min(10, len(occlist))):
        print("{};{};{:.1%}".format(occnames[occlist[i][0]], occlist[i][1], occlist[i][1]/total))
    
    
    """
    
    s = f.readline()
    i = int(s.strip())
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
    """
    

if __name__ == '__main__':
    main()