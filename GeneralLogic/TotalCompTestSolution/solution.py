# -- Solution to the Total Compensation Test in PunchLogicTest.jsonc --
# Author: Griffin Bourdon
# Date: 11/19/2022

# -- rates/wages notes --
# 0-40 hours  = regular time
# 41-48 hours = overtime
# 49+ hours   = double time

# -- job rate information -- 
#   Hospital - Painter
#       -> Rate: $31.25/hr
#       -> Benefits Rate: $1/hr

#   Hospital - laborer
#       -> Rate: $20.00/hr
#       -> Benefits Rate: $0.50/hr

#   Shop - laborer
#       -> Rate: $16.25/hr
#       -> Benefits Rate: $1.25/hr

# -- Desired output for each employee --
# -> Regular Hours (cannot exceed 40 hours)
# -> Overtime Hours (hours that exceeded 40)
# -> Double Time Hours (hours that exceeded 48)
# -> Wage Total (total amount paid to employee based on rate, including overtime/doubletime)
# -> Benefits Total (total amount paid to employee based on benefits rate)

import json, os, sys
from datetime import datetime, date, timedelta

# function to calculate the total amount of hours worked given a start and end date
def getHours(start, end):
    duration = (end - start)
    seconds  = duration.total_seconds()
    minutes  = (seconds/60)
    hours    = (minutes/60)
    return hours

# function to calculate the wage total given the amount of regular, overtime, and doubletime hours as well as the rate of the job
def calculateWageTotal(regular, overtime, doubletime, rate, overtimeRate, doubletimeRate):
    regularTotal    = (regular * rate)
    overtimeTotal   = (overtime * rate * overtimeRate)
    doubletimeTotal = (doubletime * rate * doubletimeRate)

    return (regularTotal + overtimeTotal + doubletimeTotal)

# function to calculate the total benefit given the hours and rate
def calculateBenefitTotal(hours, benefitsRate):
    return hours * benefitsRate

# main function of the program
def main():
    # constant formats & rates for the duration of the program
    FORMAT          = '%Y-%m-%d %H:%M:%S'
    DECMIAL_FORMAT  = '{0:.4f}'
    OVERTIME_RATE   = 1.5
    DOUBLETIME_RATE = 2.0

    # structure to hold the output result
    result = {}

    # opening the json input data in parsable format
    filename = 'inputData.json'
    file     = open(os.path.join(sys.path[0], filename))
    data     = json.load(file)

    # data structure to hold job objects. 
    # NOTE: the input meta data is stored as an array of jobs, so for easier access when calculating
    # each employees wages, I decided to use a lookup table. I am assuming each job title is unique.
    jobTable = {}

    # looping over job meta data in the input
    for j in data['jobMeta']:
        title        = j['job']
        rate         = j['rate']
        benefitsRate = j['benefitsRate']

        # adding the job to the table for easier access later
        jobTable[title] = {'rate': rate, 'benefitsRate': benefitsRate}
    
    # looping over employee meta data in the input
    for e in data['employeeData']:
        # total variables used for result
        wageTotal       = 0.0
        benefitTotal    = 0.0
        regularTotal    = 0.0
        overtimeTotal   = 0.0
        doubletimeTotal = 0.0
        totalHours      = 0.0

        # getting name of employee
        employeeName = e['employee']

        # looping over each time punch for current employee
        for punch in e['timePunch']:
            # temp variables for regular, overtime, and doubletime hours based on current punch
            regular      = 0.0
            overtime     = 0.0
            doubletime   = 0.0

            # time punch data
            title = punch['job']
            start = punch['start']
            end   = punch['end']

            # getting total hours for this punch
            hours = getHours(
                datetime.strptime(start, FORMAT),
                datetime.strptime(end, FORMAT)
            )

            # getting rates
            rate         = jobTable[title]['rate']
            benefitsRate = jobTable[title]['benefitsRate']

            # logic to calculate the amount of regular, overtime, and doubletime hours which
            # need to be applied to the overall wage total based on the current job rate for the current punch.

            #   -- There are 4 cases which need to be accounted for --

            # CASE 1: All of the hours worked in the current punch are regular hours
            if totalHours + hours <= 40:
                regular = hours

            # CASE 2: The amount of hours worked in the current punch is split between regular and some overtime
            elif totalHours + hours <= 48:
                regular  = 40 - totalHours
                overtime = (totalHours + hours) - 40

            # CASE 3: The amount of hours worked in the current punch is split between overtime and some doubletime
            elif totalHours < 48:
                overtime    = 48 - totalHours
                doubletime  = (totalHours + hours) - 48

            # CASE 4: The amount of hours worked in the current punch are all doubletime hours
            else:
                doubletime = hours
            
            # adding to the wage and benefit totals using the helper functions defined above
            wageTotal       += calculateWageTotal(regular, overtime, doubletime, rate, OVERTIME_RATE, DOUBLETIME_RATE)
            benefitTotal    += calculateBenefitTotal(hours, benefitsRate)

            # adding to the hour totals
            totalHours      += hours
            regularTotal    += regular
            overtimeTotal   += overtime
            doubletimeTotal += doubletime

        # creating a new employee structure to store in result 
        employee = {}
        employee['employee']     = employeeName
        employee['regular']      = str(DECMIAL_FORMAT.format(regularTotal))
        employee['overtime']     = str(DECMIAL_FORMAT.format(overtimeTotal))
        employee['doubletime']   = str(DECMIAL_FORMAT.format(doubletimeTotal))
        employee['wageTotal']    = str(DECMIAL_FORMAT.format(wageTotal))
        employee['benefitTotal'] = str(DECMIAL_FORMAT.format(benefitTotal))

        # storing employee in result output
        result[employeeName] = employee

    # printing the output as a json object like the example    
    print(json.dumps(result, indent=True))

if __name__ == '__main__':
    main()