# @Time : 2020/5/12 11:40 

# @Author : songshangru

# @File : lib.py 

# @Software: PyCharm
import time

def get_string_similarity(string_1, string_2, if_big=0, if_sym=0):
    # 将字符串变为小写
    if if_big == 0:
        string_1 = string_1.lower()
        string_2 = string_2.lower()

    string_1 = list(string_1)
    string_2 = list(string_2)

    # 去掉非字母符号
    if if_sym == 0:
        string_no_sym_1 = ''
        string_no_sym_2 = ''
        for n in string_1:
            if n.isdigit() or n.isalpha():
                string_no_sym_1 += n
        for n in string_2:
            if n.isdigit() or n.isalpha():
                string_no_sym_2 += n
    elif if_sym == 1:
        string_no_sym_1 = string_1
        string_no_sym_2 = string_2


    # 计算长度
    string_len_1 = len(string_no_sym_1)
    string_len_2 = len(string_no_sym_2)

    # 短的作为主串
    if string_len_1 > string_len_2:
        string_no_sym_1, string_no_sym_2 = string_no_sym_2, string_no_sym_1
        string_len_1, string_len_2 = string_len_2, string_len_1

    string_com = ''

    # 进行比较
    for i in range(len(string_no_sym_1)):
        if string_no_sym_1[:i] in string_no_sym_2:
            string_com = string_no_sym_1[:i+1]

    # 计算相似度
    string_com_len = len(string_com)
    similarity = string_com_len / string_len_2

    if similarity > 0.9:
        return True
    else:
        return False

if __name__ == '__main__':
    string_1 = "image_index"
    string_2 = "Image Index"
    get_string_similarity(string_1, string_2)


