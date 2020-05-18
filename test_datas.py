# @Time : 2020/5/18 15:59 

# @Author : songshangru

# @File : test_datas.py 

# @Software: PyCharm

"""
用于查询语句测试
"""
# 关键字查询
key_search = {
    "test_sets_1": {
        'field': "finding_labels",
        'key_word': ['Nodule', 'Mass']
    },
    "test_sets_2": {
        'field': "image_index",
        'key_word': ['00000105_005', '00000224_001']
    }
}
# 大小查询
size_search = {
    "test_sets_1": {
        'field': "patient_age",
        'key_word': ['100', '10000']
    },
    "test_sets_2": {
        'field': "patient_id",
        'key_word': ['50', '100']
    }
}
# 范围查询
range_search = {
    "test_sets_1": {
        'field': "patient_age",
        'key_word': ['100', '10000']
    },
    "test_sets_2": {
        'field': "patient_id",
        'key_word': ['50', '100']
    }
}