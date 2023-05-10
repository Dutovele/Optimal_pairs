import re  # we are going to use regex library so we import it on the top

# we define the important variables that we will need in the code
num_lines = 0 # number of lines we need to process
textlines = [] # the container for all lines in the input
expeditions = [] # here we will save all our final expeditions
taken_days = [False]*366 # this is a list where we mark the days which are occupied with excursions (begin or end day)
free = 7 # the minimum free days that must be between two excursions

# We create a list of numbers which represent the length of each month.
# First 0 is there just because we count from 0 in python but we need the months 1-12
month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# Later we precompute the number of days that passed before the first day of the following month
# For example, before Feb,1 there were 31 days of the year, before March,1 there are 31+28 days, before April,1 there are 31+28+31 days etc
prev_days = [sum(month_days[0:j]) for j in range(len(month_days))]
# print(prev_days)


# This function reads the lines of the file automatically
def get_inputs_from_file(dir):
    global num_lines
    global textlines

    line_number = 0
    file = open(dir, 'r')
    for line in file:
        if line_number == 0:
            num_lines = int(line)
        else:
            if line != "\n":
                temp_line = line.strip("\n")
                textlines.append(temp_line)

        line_number += 1
    file.close()

# This function reads the lines of the input
def get_input():
    global num_lines
    global textlines

    num_lines = int(input())
    for i in range(num_lines):
        line = input().strip("\n")
        if line != "\n":
            textlines.append(line)


# This helping function which calculates the days from the beginning of the year
def count_days(date):
    pieces = date.split('.') # we take the date in string form 'DD.MM' and split into ['DD', 'MM']
    day, mon = int(pieces[0]), int(pieces[1]) # we save the 'DD' as integer into day variable and 'MM' as integer into mon variable
    return day + prev_days[mon] # we return the value which is == day number + number of days before the given month
    # for example, if date is 15.02 we return 15 + 31, if date is 7.04 = 7+(31+28+31)

# This function finds the dates on a line
def get_dates():
    global textlines
    global expeditions

    # pattern1 searches for DM dates - we get first accurate DM
    # Here we create a regex pattern in order to find the dates in format "DD.MM."
    pattern = re.compile(r"((\s|^)(3[01]|[12][0-9]|[1-9])\.(1[012]|[1-9])\.)")

    '''
    (\s|^) - the character in front of the group is either space or beginning of the line
    DD 
    (3[01] | [12][0-9] | [1-9]) date is 30/31 OR 10/11/12/13..20/21/22...29  OR 1/2...9
    (1[012] | [1-9])  month is  10/11/12 OR 1..9 
    \. means the dot
    
    '''
    # Now we go the lines one by one
    for i in range(len(textlines)):
        line = textlines[i].replace(",", "") # we replace all commas on each line with "nothing" so we save filtering time
        # print(line)
        date = pattern.findall(line)  # we save all dates from the line in a list
        if len(date) != 0:  # in case the list is not empty (i.e. there is a date on the line)
            for d in range(len(date)):  # we go through each date in the list of dates
                # print(date[d])
                if int(date[d][2]) > month_days[int(date[d][3])]: #if day of the month is not valid, the whole date is removed
                    # the date is not valid if number of days for the given month is more than possible. For example, Feb has 28 days and we have 30.02 date
                    # if there is an error such that we remove that date from the list
                    date.remove(date[d])

            for item in range(len(date)): # here we go again through the dates (now the clean ones - all dates are valid
                # print(date[item][0])
                date[item] = [count_days(date[item][0]), date[item][0]] # we change the format of the date
                # the first item in data represents the number of days from the beginning of the year, and the second is the date itself

            date.sort() # we sort the date so that the dates on each line appear from earliest to the latest
            # print("The date", date)

            # now the dates are already sorted and we can choose the dates of excursions
            if len(date)!= 0: # if dates list is not empty
                # print(date[0][0], date[-1][0])
                start = date[0][0] # we chose the very first one as the start date of the trip
                end = date[-1][0] # we chose the very last one as the end date of the trip (If there is only one date on line start==end date)
                # we save the excursion dates of the line in the format we need and append it to excursions container
                # The format is [ line index, begin date of expedition (in days from start of the year), end date of expedition (in days from start of the year, date of exp]
                exp = [i+1, start, end, date[0][1].strip(" ") + " " + date[-1][1].strip(" ")]
                # print("Expedition on line", i+1, "is ", exp)
                expeditions.append(exp) # the container of all valid dates of expeditions from each line

def check_conditions(e1,e2):
    # the function checks if two expedition days are optimal
    global taken_days
    global free

    if e1[0] == e2[0]: # if the start days are same for two expeditions
        return False
    if e1[2] + free >= e2[1]: # if the time between two expeditions is less than 1 week (free=number of days that separates two expeditions)
        return False
    if True in taken_days[e1[2]+1: e2[1]]: # if there is an excursion starting or ending on that day already
        return False
    return True

# write a function to go through expeditions
def check_optimal(expeditions):
    global taken_days
    # global optim_expeditions

    optimal_len = 0
    for i in expeditions:
        # print("Checking", i)
        taken_days[i[1]] = True # we update that the start day is occupied by an expedition
        taken_days[i[2]] = True  # we update that the end day is occupied by an expedition

    for e1 in expeditions:
        for e2 in expeditions:
            if check_conditions(e1,e2): # we call the function to check all the conditions to filter for optimal pairs
                # print("Conditions met! ")

                pair_length = e1[2]-e1[1] + e2[2]-e2[1] + 2  # we count the number of days of expeditions
                if pair_length < optimal_len:  # if new length is less than the previous length we don´t add it
                    continue
                if pair_length > optimal_len: # if new length is equal to the previous length we say it is new optimal length
                    optimal_len = pair_length
                    # print("current Opt len", optimal_len)
                    optim_expeditions = []  # we open new container for optimal expeditions
                optim_expeditions.append([e1[1]*365 + e2[1]] + e1 + e2)  # we append the optim expedition to the container
                # each has the following form [86132, 9, 235, 239, '23.8. 27.8.', 5, 357, 357, '23.12. 23.12.']
                # [id number for filtering, 1st exped line, start day, end day, dates, 2nd exped line, start day, end day, dates]
                # print([e1[1]*365 + e2[1]] + e1 + e2)

    # print("-----")
    # now we print the result
    print(optimal_len) # the total number of days in any pair of optimal expedition pair in the input
    for op in sorted(optim_expeditions):
        # we only need to print out some parts of each optim expedition
        # [86132, 9, 235, 239, '23.8. 27.8.',  5, 357, 357, '23.12. 23.12.']
        #        ---          --------------  ---           -------------
        print(op[1], op[4], op[5], op[8])

    # print("-----")


#--------------------------------------------------
# print(taken_days)
get_inputs_from_file("./pubdata_optimal/pub01.in")
# get_input()
get_dates()
# # print(dates_container)
# clean_container()
# print(expeditions)
# print("++++")
check_optimal(expeditions)
# print(taken_days)