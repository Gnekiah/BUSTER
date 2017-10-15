#! /bin/python2.7
# -*- coding: utf-8 -*-
#
# xls(x) file to csv file, multi-shoot is supportted
#
# environment required: python 2.7, pyExcelerator
# @Xiong X. 2017/10/15

import pyExcelerator as pe
import sys


def error(info):
    es = extract_stack()
    if ERROR: print "[ERROR] <%s>" % es[-2][2], info
    exit()


def load_sheet(sheet):
    if len(sheet) != 2:
        error("sheet unrecognized.")
    sheet_name = sheet[0]
    sheet_cont = None
    col = 0
    row = 0
    for item in sheet[1]:
        row = max(row, item[0])
        col = max(col, item[1])
    sheet_cont = [[0 for i in range(col+1)] for j in range(row+1)]
    for item in sheet[1]:
        sheet_cont[item[0]][item[1]] = sheet[1].get(item)
    return sheet_name, sheet_cont


def load_xls(path):
    xlsd = []
    xls = pe.parse_xls(path)
    for sheet in xls:
        sheet_name, sheet_cont = load_sheet(sheet)
        xlsd.append([sheet_name, sheet_cont])
    return xlsd


def save_csv(sheet_name, sheet_cont, path):
    with open(path, "at") as f:
        for item in sheet_cont:
            tmp = ""
            for i in item:
                tmp += str(i) + ","
            f.write(tmp[:-1] + "\n")
    print "save sheet: %s as %s" % (sheet_name, path)


def main(path):
    xlsd = load_xls(path)
    save = path[:-4] if path[-4:] == ".xls" else path[:-5]
    cnt = 0
    if len(xlsd) > 1:
        cnt = 1
    for csv in xlsd:
        savepath = save + ".csv" if cnt == 0 else save + str(cnt) + "csv"
        save_csv(csv[0], csv[1], savepath)
        cnt += 1
    print "Completed!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "invalid parameter"
        exit()
    main(sys.argv[1])
