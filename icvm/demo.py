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
    csv_name = "bankloan.csv"
    clusters = init_dataset(csv_name)
    icvm(clusters)


def icvm_demo2():
    csv_base_name = "bankloan.csv"
    for i in range(2, 10):
        csv_name = csv_base_name[:-4] + str(i) + ".csv"
        clusters = init_dataset(csv_name)
        icvm(clusters, rstpath="icvm-result.csv")


def icvm_demo3():
    csv_base_name = "bankloan.csv"
    for i in range(2, 10):
        csv_name = csv_base_name[:-4] + str(i) + ".csv"
        clusters = init_dataset(csv_name)
        ## you can choose which algorithm that you wanna
        func = ['rmsstd','rs','gamma','ch','i','d','s','db','xb','sd','sdbw']
        icvm(clusters, rstpath="icvm-result.csv", func=func)


# xls2csv_demo()
# icvm_demo()
# icvm_demo2()
# icvm_demo3()