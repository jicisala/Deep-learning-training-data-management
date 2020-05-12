# @Time : 2020/5/8 14:21 

# @Author : songshangru

# @File : conf.py 

# @Software: PyCharm
# 数据库
"""
数据库配置信息
"""
DATABASE_CONNECT_INFORMATION = {
        "host": 'localhost',
        "user": 'root',
        "password": '123',
        "port": '3306',
        "db": 'lib_base'
    }

# 信息表
PICTURE_INFORMATION_TABLE_NAME = "picture_information"
# 选取表
PICTURE_SELECT_TABLE_NAME = 'selected_picture'


"""
路径信息
"""
# 图片路径
PICTURE_PATH = "F:\project_sources\Deep-learning-train-data-manage\训练数据\data_sets"
# 图片输出路径
OUTPUT_PICTURE_PATH = "E:\Projects\Python-projects\Deep-learning-training-data-management.git\outputs"
# 数据信息表路径
DATA_INFORMATION_PATH = 'F:\project_sources\Deep-learning-train-data-manage\训练数据\Data_Entry_2017_v2020.csv'