# -*- coding:utf8 -*-
# Author : Zhong Ling Long
# Create on : 2017 - 12 -27

import unittest
from common.base import  *
from common.interface import *


class FinanceTest(unittest.TestCase):
    "财务接口测试类"

    def setUp(self):
        get_cookie()
        print "erp财务接口测试开始"

    def tearDown(self):
        print "erp财务接口测试结束"

    def test_test(self):
        data = get_xlrd("finance.xlsx", "Sheet2")
        msg = myRequest(data[1][3], data[1][4], method=data[1][2])
        self.assertEqual(msg, 0)
        return msg

    # def finance_for(self):
    #     "财务接口测试用例"
    #     data = get_xlrd("finance.xlsx", "Sheet2")
    #     for i in range(len(data)-1):
    #         try:
    #             msg = myRequest(data[i+1][3],data[i+1][4],method=data[i+1][2])
    #             self.assertEqual(msg,0)
    #             return msg
    #         except BaseException as e:
    #             return e

if __name__ == "__main__":
    unittest.main()






