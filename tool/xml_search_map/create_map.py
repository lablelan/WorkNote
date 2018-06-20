# -*- coding:utf-8 -*-

import xlrd
import os

'''
	python版本: 3.6.5
	模块安装: pip install xlrd
	功能: 输出XLS_PATH_LIST文件夹下所有xls文件和服务端xml文件的映射关系
	written by: lanbei
'''

# xlsdata文件夹路径
XLSDATA_PATH = os.path.abspath('..').replace('\\', '/')
# 需要读取xls文件的路径
XLS_PATH_LIST = [ XLSDATA_PATH, XLSDATA_PATH+'/物品表']
# 不读取的文件
EXCLUSIVE_FILE = ['B-BOSS.xls', '成就.xls']

# 获取path路径下的后缀为postfix文件，返回文件名列表
def getPostfixFileList(path, postfix):
    return [file for file in os.listdir(path) if os.path.isfile(path + '/' + file) and file not in EXCLUSIVE_FILE and os.path.splitext(file)[1]==postfix]

# 获取xls文件的第一个sheet表格，返回一个字典
def getFirstSheetObjByXlsName(path, xls_name):
	workbook = xlrd.open_workbook(path + '/' + xls_name)
	sheet_obj = workbook.sheets()[0]
	return sheet_obj

# 获取xls对应的xml名(第一个sheet的第一列)
def getXmlnameBySheetObj(sheet_obj):
	return sheet_obj.row_values(1)[0] + '.xml'

def main():
	# 保存xls和xml的对应关系
	xls_map_xml_dict = {}  

	# 读取xls
	for xls_path in XLS_PATH_LIST:
		xls_name_list = getPostfixFileList(xls_path, '.xls')
		for xls_name in xls_name_list:
			sheet_obj = getFirstSheetObjByXlsName(xls_path, xls_name)
			xls_map_xml_dict[xls_name] = getXmlnameBySheetObj(sheet_obj)
			print(xls_name, " -> ", xls_map_xml_dict[xls_name])

	# 一次性写入xls_map_xml.txt
	with open("./xls_map_xml.txt", "w", encoding='utf-8') as f:
		for key, val in xls_map_xml_dict.items():
			print(key, " -> ", val, file=f)
	print("map has written to xls_map_xml.txt")

if __name__ == '__main__':
	main()