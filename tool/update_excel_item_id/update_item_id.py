# -*- coding:utf-8 -*- 

import xlrd
import xlwt
import os
import json
import re
from xlutils.copy import copy

'''
    批量修改格式为：item_id:is_bind:num 物品/物品列表的物品id
'''

# 获取path路径下的后缀为postfix文件名列表
def getPostfixFileList(path, postfix):
    return [file for file in os.listdir(path) if os.path.isfile(path + '/' + file) and os.path.splitext(file)[1]==postfix]

# 读取一个xls文件，返回xls的sheet名列表
def getSheetNameList(xls_name):
    workbook = xlrd.open_workbook(xls_name)
    sheet_names = workbook.sheet_names()
    return sheet_names

# 读取一个xls文件，返回xls的sheet字典
def getSheetDict(path, xls_name):
	sheet_obj_dict = { }
	workbook = xlrd.open_workbook(path + '/' + xls_name)
	sheet_names = workbook.sheet_names()
	for sheet_name in sheet_names:
		sheet_obj_dict[sheet_name] = workbook.sheet_by_name(sheet_name)

	return sheet_obj_dict

# 返回物品和物品列表单元格行列元组(row, col)列表。整型会被转成字符串
def getItemAndItemlistCellList(sheet_obj, original_item_id, target_item_id):
    cell_list = []

    nrows = sheet_obj.nrows
    for row in range(nrows):
        for col in range(len(sheet_obj.row_values(row))):
            cell_value = sheet_obj.row_values(row)[col]
            # 是浮点数或整数那就肯定不是物品id格式
            if isinstance(cell_value, float) or isinstance(cell_value, int):
                continue

            cell_value = str(cell_value)

            # 如果单元格内容是空字符串不记录
            if cell_value == '':
                continue

            # 筛选出只含有original_item_id的单元格并替换成target_item_id
            string_index = cell_value.find(original_item_id + ':')
            if string_index != -1:
                cell_value = cell_value.replace(original_item_id, target_item_id)
                cell = { (row, col) : cell_value }
                cell_list.append(cell)   
            else :
                continue
           
    return cell_list

def main():
    xls_path = 'C:/work/ug04_cn/xlsdata'
    save_path = 'C:/work/ug04_cn/xlsdata/update_excle_item_id/xls'

    item_list = []
    with open("./item_id_cfg.json", 'r') as load_f:
        load_dict = json.load(load_f)
        print(load_dict)
        item_list.append(load_dict)
    xls_list = getPostfixFileList(xls_path, '.xls')
    
    # 读取需要修改的xls表到xls_dict
    xls_dict = {}
    for item_dict in item_list:
        original_item_id = ''
        target_item_id = ''
        for key, value in item_dict.items():
            original_item_id = key
            target_item_id = value
        
            # 遍历当前文件夹xls文件
            for xls_name in xls_list:
                sheet_dict = {}
                sheet_obj_dict = getSheetDict(xls_path, xls_name)
                for sheet_name in sheet_obj_dict:
                    cell_list = getItemAndItemlistCellList(sheet_obj_dict[sheet_name], original_item_id, target_item_id)
                    # 如果单元格列表为空不记录
                    if len(cell_list) == 0:
                        continue
                    sheet_dict[sheet_name] = cell_list
                    print(xls_name, "  ", sheet_name, "  ", sheet_dict[sheet_name])
                    xls_dict[xls_name] = sheet_dict

            # 输出将修改的日志
            with open("./readlog.txt", "w", encoding='utf-8') as f:
                for xls_name in xls_dict:
                    print(xls_name, "  ", xls_dict[xls_name], file=f)
            
    # 获取xls_dict对应的xls对应的sheet对应的单元格进行修改操作
    for w_xls_name, w_sheet_dict in xls_dict.items():
        wbk = xlrd.open_workbook(xls_path + '/' + w_xls_name)
        workbooknew = copy(wbk)
        for w_sheet_name, w_cell_list in w_sheet_dict.items():
            w_sheet = workbooknew.get_sheet(w_sheet_name)
            for w_cell_dict in w_cell_list:
                for w_col_rol_tuple, w_cell_val in w_cell_dict.items():
                    w_sheet.write(w_col_rol_tuple[0], w_col_rol_tuple[1], str(w_cell_val))
        workbooknew.save(save_path + '/' + w_xls_name)


if __name__ == '__main__':
    main()
