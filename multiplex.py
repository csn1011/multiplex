
def file_opener(filename):
    """Opens file and prints error message/returns none if the file cannot be opened"""
    try:
        text_file = open(filename)
    except:
        return print("Error, file ", filename, "could not be opened")
    return text_file

def read_line(filename):
    """Reads each line of a file and converts it into  a list (line), then puts each line
        into a list of lists representing a test case (line_list), then puts each test case into
        a list of test cases (super_list) and calls timer function on super_list"""
    text_file = file_opener(filename)
    line_list = []
    super_list = []
    for line in text_file:
        if line[0] != "\n" and line[0] != "": #looks for \n character to indicate end of test case
            input_line = line.split(",")
            n = len(input_line) - 1
            input_line[n] = input_line[n].replace("\n","") #parse out '\n' character attatched to last item in a test
            line_list = line_list + [input_line]
        else:
            super_list = super_list + [line_list] #if it is the end of a test case, add test case to list of test cases
            line_list = [] #reset container for test case to empty
    timer(super_list)

def timer(super_list):
    """Takes the list of test cases and inputs them into the rest of the program
        one test case at a time to ensure order of outputs corresponds to order of
        inputs (i.e in case one case terminates early as a result of being inconsistent)"""
    for x in super_list:
        if process_line(x):
            return

def process_line(line_list):
    """Takes the nested list representing a test case and parses it into both a dictionary
        of all sample IDs in "NORM" tests and a nested list of "MUT" tests. The function
        also counts number of "NORM" samples. The function then calls the multiplex
        function on the created dictionary, list and count of normal samples"""
    dict_of_id = {}
    list_of_muts = []
    for line in line_list:
        if line[0] == "NORM":
            new_line = line[1:] #take the string "NORM" out of list representing a test
            for x in new_line:
                dict_of_id[x] = "NORM" #add a new dict key of sample ID with value "NORM"
        elif line[0] == "MUT":
            new_line = line[1:] #take the string "MUT" out of list representing a test
            list_of_muts = list_of_muts + [new_line] #add a "MUT" test to a list of "MUT" tests
        else:
            return print("First word of each line does not begin with 'MUT' or 'NORM', please reformat")
    norm_count = len(dict_of_id) #records the number of normal samples
    Multiplex (dict_of_id, list_of_muts,norm_count)

def Multiplex(dict_of_id, list_of_muts, norm_count):
    """Function that checks for consistency, uniqueness, and returns a dictionary
        of sample IDs with "MUT" or "NORM" as values"""
    if len(list_of_muts) == 0:
        output_function(dict_of_id,norm_count)
    new_list = consistency_checker(dict_of_id, list_of_muts)
    if new_list:
        new_dict = mut_adder(dict_of_id, new_list)
        if new_dict:
            if uniqueness_checker(new_dict, new_list):
                output_function(new_dict, norm_count)

def output_function(dict_of_id, norm_count):
    """Function which takes a dictionary of sample ID's who's values are "NORM" or "MUT", and orders
        the dictionary by key then prints them. Function also outputs the number of "NORM" and "MUT" samples"""
    sorted_dict = sorted(dict_of_id.items(), key = lambda t: int(t[0]))
    print("NORM COUNT:", norm_count)
    print("MUT COUNT:", len(sorted_dict) - norm_count)
    for x in sorted_dict:
        if x[1] != "NORM":
            type = "MUT"
        else:
            type = "NORM"
        print(x[0], ",", type, sep = '')
    print("")
    return

def remove_norms_or_all(list, dict, key = None):
    """Function which takes a dictionary, list, and an optional key as arguments and iterates
        through the list removing items, which are keys in the dictionary, or if specified
        only removing items who's corresponding values are equal to the 'key' argument. Returns
        edited version of the list"""
    temp = list[:] #create copy to iterate through so that the list is not modified as its being iterated through
    if key:
        for x in temp:
            if x in dict and dict[x] == key:
                list.remove(x)
    elif not key:
        for x in temp:
            if x in dict:
                list.remove(x)
    return list

def consistency_checker(dict_of_id, list_of_muts_only):
    """Checks if a "MUT" test contains all "NORM" sample IDs (prints  INCONSISTENT and
        terminates program if that's the case). Takes a list of "MUT" tests and a dictionary
        containing sample IDs that are "NORM", returns the list "MUT" tests with "NORM" sample
        IDs removed (if the "MUT" tests are not INCONSISTENT)"""
    for x in list_of_muts_only:
        x = remove_norms_or_all(x, dict_of_id, "NORM") #removes all samples from "MUT" test which are in "NORM" tests
        if len(x) == 0:
            print("INCONSISTENT") #if all samples in a "MUT" test were in "NORM" tests, test was inconsistent
            return print("")
    return list_of_muts_only

def mut_adder(dict_of_id_with_muts, list_of_muts_only):
    """Takes a dictionary of "NORM" sample IDs and a list of "MUT" tests with known "NORM"
        samples removed. Fucntion adds any sample IDs from "MUT" tests containing a
        single sample (those must be "MUT"), if they are not already in the dictionary"""
    for x in list_of_muts_only:
        if len(x) == 1:
            if x[0] not in dict_of_id_with_muts:
                dict_of_id_with_muts[x[0]] = "MUT" #if there is a consistent "MUT" test with one item that item must be "MUT"
    return dict_of_id_with_muts

def uniqueness_checker(dict_of_id_with_muts, list_of_muts_only):
    """Takes a dictionary of all known sample IDs as keys and their "NORM"/"MUT" status as
        values and a list of "MUT" tests with "NORM" sample IDs removed. Checks if any of the
        "MUT" tests contain samples that are neither known to be "NORM" nor "MUT"
        (prints "NONUNIQUE" if true)"""
    for x in list_of_muts_only:
        x = remove_norms_or_all(x, dict_of_id_with_muts) #removes all items marked "NORM" or "MUT"
        if len(x)!=0:
            print ("NONUNIQUE") #if there is an item that is neither "NORM" nor "MUT" test is nonunique
            return print("")
    return True
