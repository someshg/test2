# Table of Contents
1. [Problem](README.md#problem)
2. [Approach](README.md#approach)
3. [Running](README.md#running)

# Problem

This module takes a csv input text file which provides information about H1 visa filing for a given year. The first line is the header line and contains the names of the columns. Each subsequent line provides information about one specific visa application. The data is available from the US Department of Labor and its [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). However the data is required to be converted to csv format (with ; separator).

The first requirement is to process a file and provide reports on the top 10 Occupations and top 10 States for certified visa applications.
* The ; separated column names for the same information vary from year to year
* The status column indicates whether the application was certified or not
* There are many state columns. The one of interest is the primary work site location state
* The other column of interest is the one that contains the occupation name associated with the Standard Occupational Classification (SOC) code
* As a side note, it is assumed that the occupation name is not hand typed but an automatic selection based on code. If this is not the case, an alternative might be to process using the SOC code and in the main processing loop, pick the first name encountered for a specific code. This could avoid any miscounting due to mistakes in typing the occupation name

The output format is required to be as follows:
* summary for occupation and state are to be written to separate files
* A very specific format of the output header line is given. The code documents the format 
* for the top 10 occupations, the output contains the occupation name; number of certified applications for the occupation; and percentage of applications for the occupation as a percent of total number of certified applications
* for the top 10 states, similar information is required except grouping is by state instead of by occupation
* The output must be in descending order by count; and in case of ties in alphabetical order by occupation name or state name
### The Unspecified Requirement

It is pretty reasonable to assume that the initial request will be followed by new requests for slightly varying information. Some examples may be
* The top 20 states
* output all the occupations instead of the top 10
* Similar summary as the initial requirement but for applications that were not certified
* the top 10 employer names requesting visas

While all of the requirements cannot be anticipated, it is important that the design approach be flexible without programming up-front for the unknown requirements


# Approach

The basic idea in the design is to use definitions to drive the program.
* As an example, the word application "status" for column/field appears only in constant definitions and not in the code instructions. Similarly the various strings that indicate application status (such as "CASE_STATUS", "STATUS", "APPROVAL_STATUS") are in a lsit in constant definitions.
* What that means is that if in 2019, the column is known by a different name, then only the constant definition needs to be extended with the new string and nothing else has to change
* Similarly if there is a need to tally up the applications with the status "Denied", then only the definition of the constant KEY_VALUE has to change

At the same time, there was no code specifically added for future requirements. For example, if there is new requirement to provide the same data for all applications regardless of status, then some minor modification do need to be made to the code. For example, a new constant MATCH_TYPE may be added with values of MATCH, DOES_NOT_MATCH or NO_MATCH_NEEDED and some minor corresponding code modification has to made

The following are the important constants used to drive the code

* COLUMN_DEFS is a dictionary that contains all the columns used in the computation. The key is a common column name such as "state" or "status" or "soc_name" and the values correspond to a list of strings which each of these columns may actually be known by in different years.
* KEY_NAME and KEY_VALUE are the column used for matching (currently "status") and the value for that column to match on (currently "CERTIFIED")
* The OUT_STRINGS is the dictionary - one key-value pair for every file to be output and should follow the order of the output files in the command line.
* The OUT_COUNT is how many maximum values in descending order should be written out (10 for the first phase)

## Brief Overview of the code

* The code first processes the header line in the input file. It uses the COLUMN_DEFS to find the index of the columns of interest - only exact matches for any of the strings by which a column is known are supported.
* If any of the columns are not found in the header line, the code prints an error to the standard output and returns without further processing
* It then goes through the input file line by line - for processing optimization, it processes a line only if the match rule passes and then extracts the values in the columns of interest
* A dictionary where the values are themselves dictionaries is used to store the results. The key at the first level is the column name. The second level dictionary contains e.g. the state names encountered and the value is the count of applications for that state
* The second level dictionary data is converted to a list of tuples for ease of sorting. The sorting is done in alpbabetical order first (ascending) and then by count (descending)
* Since python sort is stable sort, if there are two states or occupations with the same count, the order will remain alphabetical order
* The data is then written to the output files in the format specified. The formatting code chosen provided the appropriate rounding for percentage

# Running 

The command line for executing the program is as per the run.sh script

python3 ./src/h1b_counting.py <input_file> <output_file_for_occuptations> <output_file_for_states>

If the columns are not found or the input file cannot be opened or the expected number of output
files is not specified, the program prints an error to stdout and returns
