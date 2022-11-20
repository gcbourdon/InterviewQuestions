# -- Unit test cases for the solution to Total Compensation Test in PunchLogicTest.jsonc --
# Author: Griffin Bourdon
# Date: 11/20/2022

import unittest, solution
from datetime import datetime

class TestSolutionFunctions(unittest.TestCase):

    # CASE 1: All of the hours worked in the current punch are regular hours
    def test_hours_1(self):
        # so far, the total amount of hours worked is 30. By adding a 10 hour shift, the total becomes 40. This means 10 regular hours were worked. 
        result   = solution.get_hours(30, 10)
        expected = {
            'regular': 10,
            'overtime': 0,
            'doubletime': 0
        }
        self.assertEqual(result['regular'], expected['regular'])
        self.assertEqual(result['overtime'], expected['overtime'])
        self.assertEqual(result['doubletime'], expected['doubletime'])

    # CASE 2: The amount of hours worked in the current punch is split between regular and some overtime
    def test_hours_2(self):
        # so far, the total amount of hours is 38. By adding a 4 hour shift, the total becomes 42. This means 2 hours of regular and 2 overtime hours were worked.
        result   = solution.get_hours(38, 4)
        expected = {
            'regular': 2,
            'overtime': 2,
            'doubletime': 0
        }
        self.assertEqual(result['regular'], expected['regular'])
        self.assertEqual(result['overtime'], expected['overtime'])
        self.assertEqual(result['doubletime'], expected['doubletime'])
 
    # CASE 3: the amount of hours worked in the current punch is split between overtime and some doubletime
    def test_hours_3(self):
        # so far, the total amount of hours is 45. By adding a 8 hour shift, the total becomes 53. This means 3 hours of overtime and 5 hours of doubletime were worked.
        result   = solution.get_hours(45, 8)
        expected = {
            'regular': 0,
            'overtime': 3,
            'doubletime': 5
        }
        self.assertEqual(result['regular'], expected['regular'])
        self.assertEqual(result['overtime'], expected['overtime'])
        self.assertEqual(result['doubletime'], expected['doubletime'])


    # CASE 4: The amount of hours worked in the current punch are all doubletime hours
    def test_hours_4(self):
        # so far, the total amount of hours is 48. By adding a 6 hour shift, the total becomes 54. This means that 6 hours of doubletime were worked.
        result   = solution.get_hours(48, 6)
        expected = {
            'regular': 0,
            'overtime': 0,
            'doubletime': 6
        }
        self.assertEqual(result['regular'], expected['regular'])
        self.assertEqual(result['overtime'], expected['overtime'])
        self.assertEqual(result['doubletime'], expected['doubletime'])

    # unit test for calculating the wage total given only regular hours
    def test_wage_total_1(self):
        # for someone that worked 40 regular hours at an hourly rate of $31.25, we should expect their wage to be $1,250
        result   = solution.get_wage_total(40, 0, 0, 31.25, 1.5, 2.0)
        expected = 1250
        self.assertEqual(result, expected)

    # unit test for calculating wage total given regular and overtime hours
    def test_wage_total_2(self):
        # for someone that worked 40 regular hours and 5.4 overtime hours at an hourly rate of $20, we should expect their wage to be $962
        result   = solution.get_wage_total(40, 5.4, 0, 20, 1.5, 2.0)
        expected = 962
        self.assertEqual(result, expected)
    
    # unit test for calculating wage total given regular, overtime, and doubletime hours
    def test_wage_total_3(self):
        # for someone that worked 40 regular hours, 8 overtime hours, and 4.25 doubletime hours at an hourly rate of $42.75, we should expect their wage to be $2,586.375
        result   = solution.get_wage_total(40, 8, 4.25, 42.75, 1.5, 2.0)
        expected = 2586.375
        self.assertEqual(result, expected)
    
    # unit test for base pay
    def test_base_wage(self):
        result   = solution.get_base_wage(40, 42.75)
        expected = 1710
        self.assertEqual(result, expected)

    # unit test for overtime pay
    def test_overtime_wage(self):
        result   = solution.get_overtime_wage(8, 42.75, 1.5)
        expected = 513
        self.assertEqual(result, expected)
    
    # unit test for doubletime pay
    def test_doubletime_wage(self):
        result   = solution.get_doubletime_wage(4.25, 42.75, 2.0)
        expected = 363.375
        self.assertEqual(result, expected)

    # unit test for benefits total
    def test_benefit_total(self):
        result   = solution.get_benefit_total(30, 1.25)
        expected = 37.5
        self.assertEqual(result, expected)

    # unit test for calculating duration of hours worked given start and end date
    def test_hours_worked(self):
        format   = '%Y-%m-%d %H:%M:%S'
        start    = '2022-11-18 08:02:20'
        end      = '2022-11-18 16:15:40'
        result   = round(solution.get_hours_worked(datetime.strptime(start, format), datetime.strptime(end, format)), 4)
        expected = 8.2222
        self.assertEqual(result, expected)
        
if __name__ == '__main__':
    unittest.main()