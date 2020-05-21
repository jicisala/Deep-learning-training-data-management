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

TABLE = {
    # 信息表
    'DATA_INFORMATION': "picture_information",
    # 信息表
    'DATA_SELECT': 'selected_picture',
}

"""
路径信息
"""
PATH = {
    # 数据路径
    'DATA': "F:\project_sources\Deep-learning-train-data-manage\训练数据\data_sets",
    # 数据输出路径
    'DATA_OUTPUT': "F:\project_sources\Deep-learning-train-data-manage\Outputs",
    # 数据信息表路径
    'DATA_INFORMATION': 'F:\project_sources\Deep-learning-train-data-manage\训练数据\Data_Entry_2017_v2020.csv',
}
