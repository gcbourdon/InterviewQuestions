# -- Solution to the Total Compensation Test in PunchLogicTest.jsonc --
# Author: Griffin Bourdon
# Date: 11/20/2022

import json, os, sys
from datetime import datetime, date, timedelta

# function to calculate the total amount of hours worked given a start and end date
def get_hours_worked(start, end):
    duration = (end - start)
    seconds  = duration.total_seconds()
    minutes  = (seconds/60)
    hours    = (minutes/60)
    return hours

# function to calculate the regular, overtime, and doubletime hours worked given the total hours worked and hours for the shift
def get_hours(totalHours, hours_worked):
    # temp values to store in result 
    regular     = 0.0
    overtime    = 0.0
    doubletime  = 0.0
    result      = {
        'regular': regular,
        'overtime': overtime,
        'doubletime': doubletime
    }

    #   -- There are 4 cases which need to be accounted for --

    # CASE 1: All of the hours worked in the current punch are regular hours
    if totalHours + hours_worked <= 40:
        regular = hours_worked

    # CASE 2: The amount of hours worked in the current punch is split between regular and some overtime
    elif totalHours + hours_worked <= 48:
        regular  = 40 - totalHours
        overtime = (totalHours + hours_worked) - 40

    # CASE 3: the amount of hours worked in the current punch is split between overtime and some doubletime
    elif totalHours < 48:
        overtime    = 48 - totalHours
        doubletime  = (totalHours + hours_worked) - 48

    # CASE 4: The amount of hours worked in the current punch are all doubletime hours
    else:
        doubletime = hours_worked
    
    # building the result and returning
    result['regular']    = regular
    result['overtime']   = overtime
    result['doubletime'] = doubletime

    return result

# function to calculate the wage total given the amount of regular, overtime, and doubletime hours as well as the rate of the job
def get_wage_total(regular, overtime, doubletime, rate, overtimeRate, doubletimeRate):
    baseTotal       = get_base_wage(regular, rate)
    overtimeTotal   = get_overtime_wage(overtime, rate, overtimeRate)
    doubletimeTotal = get_doubletime_wage(doubletime, rate, doubletimeRate)

    return baseTotal + overtimeTotal + doubletimeTotal

# function to calculate the base wage given regular hours worked and an hourly rate
def get_base_wage(regular, rate):
    return regular * rate

# function to calculate the overtime wage given overtime hours worked, hourly rate, and overtime rate
def get_overtime_wage(overtime, rate, overtimeRate):
    return overtime * rate * overtimeRate

# function to calculate the doubletime wage given doubletime hours worked, hourly rate, and doubletime rate
def get_doubletime_wage(doubletime, rate, doubletimeRate):
    return doubletime * rate * doubletimeRate

# function to calculate the total benefit given the hours and rate
def get_benefit_total(hours, benefitsRate):
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
    # each employees wages, I decided to use a seperate key/value object. I am assuming each job title is unique.
    jobTable = {}

    # looping over job meta data in the input
    for j in data['jobMeta']:
        title        = j['job']
        rate         = j['rate']
        benefitsRate = j['benefitsRate']

        # adding the job to the table for easier access later
        jobTable[title] = {
            'rate': rate, 
            'benefitsRate': benefitsRate
        }
    
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
            # time punch data
            title = punch['job']
            start = punch['start']
            end   = punch['end']

            # getting total hours worked for this punch
            hours_worked = get_hours_worked(datetime.strptime(start, FORMAT), datetime.strptime(end, FORMAT))

            # getting rates
            rate         = jobTable[title]['rate']
            benefitsRate = jobTable[title]['benefitsRate']

            # getting the regular, overtime, and doubletime hours worked for this punch
            hours       = get_hours(totalHours, hours_worked)
            regular     = hours['regular']
            overtime    = hours['overtime']
            doubletime  = hours['doubletime']

            # adding to the wage and benefit totals using the helper functions defined above
            wageTotal       += get_wage_total(regular, overtime, doubletime, rate, OVERTIME_RATE, DOUBLETIME_RATE)
            benefitTotal    += get_benefit_total(hours_worked, benefitsRate)

            # adding to the hour totals
            totalHours      += hours_worked
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