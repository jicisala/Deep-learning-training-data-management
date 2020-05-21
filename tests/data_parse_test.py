# @Time : 2020/5/21 14:57 

# @Author : songshangru

# @File : data_parse_test.py 

# @Software: PyCharm
from core import data_parse


data_path_json = r"E:\Projects\Python-projects\Deep-learning-training-data-management.git\tests\test_data\json"
data_type_json = 'json'

data_type_csv = "csv"
data_path_csv = r"E:\Projects\Python-projects\Deep-learning-training-data-management.git\tests\test_data\Data_Entry_2017_v2020.csv"

data_type_excel = 'excel'
data_path_excel = ''

data_type_fault = 'dog_son'


# 报错测试
test_object_fault = data_parse.DataParse(data_path=data_path_csv)

# csv测试
csv_result = data_parse.DataParse(data_path=data_path_csv).parse_csv(1)
print(csv_result)

# json测试
json_result = data_parse.DataParse(data_path=data_path_json).parse_json()
print(json_result)

# excel解析
test_object_excel = data_parse.DataParse(data_path=data_path_excel)