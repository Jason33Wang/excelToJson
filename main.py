# -*- coding: utf-8 -*-
# 这段代码主要的功能是把excel表格转换成utf-8格式的json文件
import os
import sys
import codecs
import xlrd
import xdrlib
import json
from importlib import reload
reload(sys)


# sys.setdefaultencoding( "utf-8" )
def open_ecxcel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception :
        print("has wrong")

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file,colnameindex=0,by_name=u'AIS动态信息'):
    data = open_ecxcel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows
    print(nrows)
    colnames = table.row_values(colnameindex)
    records = []
    for rownum in range(1,nrows):
        row = table.row_values(rownum)
        if row[0]:
            record = {}
            for i in range(len(colnames)):
                #excel 默认float ,强制类型转换
                if type(row[i]) == float:
                    row[i] = int(row[i])
                    row[i] = str(row[i])
                record[colnames[i]] = row[i]
        records.append(record)
    return records

#open_ecxcel('wzsj.xlsx')
recodes = excel_table_byname('data1.xls')
encodedjson = json.dumps(recodes,ensure_ascii=False,indent=2)
#encodedjson = json.dumps(recodes)
print(encodedjson)
output = open('data11.json', 'w+')
output.write(encodedjson)

#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file,colnameindex=0,by_index=0):
    data = open_ecxcel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据
    records = []
    for rownum in range(1,nrows):

         row = table.row_values(rownum)
         if row:
             record = {}
             for i in range(len(colnames)):
                record[colnames[i]] = row[i]
             records.append(record)
    return records