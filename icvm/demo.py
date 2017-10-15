#! /bin/python2.7
# -*- coding: utf-8 -*-
#
# demo for using 'icvm' and 'xls2csv'
#
# environment: python 2.7 is recommended
# @Xiong X. 2017/10/15

from icvm import init_dataset, icvm
from xls2csv import xls2csv


def xls2csv_demo():
    xls_base_name = "bankloan.xls"
    for i in range(2, 10):
        xls_name = xls_base_name[:-4] + str(i) + ".xls"
        xls2csv(xls_name)
    print "All format conversion completed!"


def icvm_demo():
    csv_base_name = "bankloan.csv"
    for i in range(2, 10):
        csv_name = csv_base_name[:-4] + str(i) + ".csv"
        clusters = init_dataset(csv_name)
        icvm(clusters, "icvm-result.csv")


# xls2csv_demo()
# icvm_demo()
