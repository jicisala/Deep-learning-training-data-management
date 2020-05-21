# @Time : 2020/5/21 14:49 

# @Author : songshangru

# @File : data_parse.py 

# @Software: PyCharm
"""
将各种格式的数据解析成标准的python字典格式
:return:字典格式
"""
import conf


class DataParse:
    def __init__(self, data_path=conf.PATH["DATA_INFORMATION"]):
        self.data_path = data_path

    def parse_csv(self, output_type= 2):
        """
        解析csv文件，为了能兼容之前版本的数据管理，所以加了类型字段，
        :param output_type:
        :param type: 0为列表的属性行，1为列表的值，2为字典形式
        :return:
        """
        import csv

        with open(self.data_path, 'r') as contents:
            reader = list(csv.reader(contents))
            data_fields = reader[0]
            data_values = reader[0:]
        if output_type == 1:
            # 去掉第一行属性名行
            result = list(reader)[1:]
        elif output_type == 0:
            result = list(reader)[0]
        elif output_type == 2:
            # 拼接成字典
            data_dict = {}
            data_length = len(data_values)

            for n in range(data_length):
                data_dict[n] = {}
                for m in range(len(data_fields)):
                    data_dict[n][data_fields[m]] = data_values[n][m]

            result = [data_dict, data_fields]

        return result

    def parse_json(self):
        """
        解析json格式的数据
        :return:
        """
        import json
        with open(self.data_path, 'r') as contents:
            json_data = json.load(contents)

        return json_data


    def parse_excel(self):
        print("开始解析excel...\n骗你的，我还没写")


