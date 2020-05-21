# @Time : 2020/5/13 14:27 

# @Author : songshangru

# @File : main_test.py

# @Software: PyCharm
import main
import conf
from tests.test_data import test_data_sql
import random
from core.database.database import DatabaseHandle


# 测试主模块
class TrainDataHandleTest:
    def __init__(self):
        try:
            self.test_object_traindatahandle = main.TrainDataHandle()
        except BaseException:
            print("数据库连接失败")
            self.print_separator()
        else:
            print("数据库连接成功")
            print("主机地址为：" + conf.DATABASE_CONNECT_INFORMATION['host'] + '\n' +
                  "登陆用户为：" + conf.DATABASE_CONNECT_INFORMATION['user'] + '\n' +
                  "登陆端口为：" + conf.DATABASE_CONNECT_INFORMATION['port'] + '\n' +
                  '使用的数据库为：' + conf.DATABASE_CONNECT_INFORMATION['db'] + '\n')
            self.print_separator()

    """
    辅助函数区
    """

    # 获取配置文件中的表名
    def get_table_name(self):
        table_names = []
        for key in conf.TABLE:
            table_names.append(conf.TABLE[key])

        return table_names

    # 输出一行分割符
    def print_separator(self):
        print("***********************************************************************")

    """
    测试函数区
    """

    # 测试数据表字段获取
    def test_get_fields(self):
        table_names = self.get_table_name()

        for table_name in table_names:
            filed_results = self.test_object_traindatahandle.get_fields(table_name=table_name)
            if not filed_results:
                print('数据字段为空')
            else:
                print("表" + table_name + "的字段为：\n" + str(filed_results) + "\n")

        self.print_separator()

    # 测试sql语句构建
    def test_sql_construct(self):
        table_names = self.get_table_name()
        introduce = ''

        for table_name in table_names:
            for sql_type in range(1, 4):
                if sql_type == 1:
                    introduce = "构造的插入语句为："
                elif sql_type == 2:
                    introduce = "构造的查询语句："
                elif sql_type == 3:
                    introduce = "构造的删除语句为："
                else:
                    print("sql_type范围错误")

                sql_construct = self.test_object_traindatahandle.construct_sql(table_name, sql_type)
                print("表" + table_name + introduce + '\n' + sql_construct + '\n')

        self.print_separator()

    # 测试主数据表写入
    def test_input_data(self):
        self.test_object_traindatahandle.input_data()

        self.print_separator()

    # 测试数据的三种查询（关键字，大小，范围）
    def test_search_data_key(self):
        # 获得关键字
        for test_set_name in test_data_sql.key_search:
            test_set_value = test_data_sql.key_search[test_set_name]

            # 获得详细信息
            test_set_value_field = test_set_value['field']
            test_set_value_key_words = test_set_value['key_word']

            # 精确查询
            for test_set_value_key_word in test_set_value_key_words:
                search_result = self.test_object_traindatahandle.search_data_key(field=test_set_value_field,
                                                                 key_word=test_set_value_key_word, if_like=0)
                if search_result:
                    print(str(test_set_value_field) + "字段查询关键字" + str(test_set_value_key_word) + "的精确查询结果为：" + str(
                        search_result))
                else:
                    print(str(test_set_value_field + "字段查询关键字" + str(test_set_value_key_word) + "结果为空"))

            self.print_separator()

            for test_set_value_key_word in test_set_value_key_words:
                search_result_like = self.test_object_traindatahandle.search_data_key(field=test_set_value_field,
                                                                      key_word=test_set_value_key_word, if_like=1)
                if search_result_like:
                    print(str(test_set_value_field) + "字段查询关键字" + str(test_set_value_key_word) + "的模糊查询结果为：" + str(
                        search_result_like))
                else:
                    print(str(test_set_value_field + "字段查询关键字" + str(test_set_value_key_word) + "结果为空"))

        self.print_separator()

    def test_search_data_size(self):
        # 获得关键字
        for test_set_name in test_data_sql.size_search:
            test_set_value = test_data_sql.size_search[test_set_name]

            # 获得详细信息
            test_set_value_field = test_set_value['field']
            test_set_value_key_words = test_set_value['key_word']

            # 大小查询
            for test_set_value_size_word in test_set_value_key_words:
                search_result = self.test_object_traindatahandle.search_data_size(field=test_set_value_field,
                                                                  key_word=test_set_value_size_word, com_type='>')
                if search_result:
                    print(str(test_set_value_field) + "大小查询关键字" + str(test_set_value_size_word) + "的大于查询结果为：" + str(
                        search_result))
                else:
                    print(str(test_set_value_field + "大小查询关键字" + str(test_set_value_size_word) + "结果为空"))

        self.print_separator()

    def test_search_data_range(self):
        # 获得关键字
        for test_set_name in test_data_sql.range_search:
            test_set_value = test_data_sql.range_search[test_set_name]

            # 获得详细信息
            test_set_value_field = test_set_value['field']
            test_set_value_key_words = test_set_value['key_word']

            test_set_value_range_word_1 = test_set_value_key_words[0]
            test_set_value_range_word_2 = test_set_value_key_words[1]

            # 范围查询
            search_result = self.test_object_traindatahandle.search_data_range(field=test_set_value_field,
                                                               key_word_1=test_set_value_range_word_1,
                                                               key_word_2=test_set_value_range_word_2,
                                                               )
            if search_result:
                print(str(test_set_value_field) + "范围查询关键字" + str(test_set_value_range_word_1) + "到" + str(
                    test_set_value_range_word_2) + "的范围查询结果为：" + str(
                    search_result))
            else:
                print(str(test_set_value_field + "范围查询关键字" + str(test_set_value_range_word_1) + "到" + str(
                    test_set_value_range_word_2) + "的范围查询结果为空"))

        self.print_separator()

    # 测试避免重复功能
    def test_duplicate_avoid(self):
        key_word = random.randint(1, 94)
        # 数据插入
        search_result = self.test_object_traindatahandle.search_data_key(field='patient_age', key_word=key_word, if_like=0)
        self.test_object_traindatahandle.duplicate_avoid(search_result)

        # 数据查询
        # 获得选中表记录
        sql = "SELECT * FROM selected_picture order by id desc limit 1"
        self.test_object_traindatahandle.cursor.execute(sql)
        search_result_selected_result = self.test_object_traindatahandle.cursor.fetchall()

        if search_result[0][0] == search_result_selected_result[0][1]:
            print("去重功能有效")
        else:
            print("去重功能无效")

        self.print_separator()

    # 测试数据输出
    def test_output_data(self):
        key_word = random.randint(1, 94)
        # 数据插入
        search_result = self.test_object_traindatahandle.search_data_key(field='patient_age', key_word=key_word, if_like=0, nums=10)
        self.test_object_traindatahandle.output_data(search_result)

        self.print_separator()

    # 测试初始化功能
    def test_initialization(self):
        self.test_object_traindatahandle.initialization()

        self.print_separator()

    # 测试中途数据写入的去重
    def test_input_selected_data_to_selected_table(self):
        self.test_object_traindatahandle.input_selected_data_to_selected_table()

        self.print_separator()

    def test(self, if_input=0):
        self.test_object_traindatahandle = TrainDataHandleTest()
        self.test_object_traindatahandle.test_get_fields()
        self.test_object_traindatahandle.test_sql_construct()
        if if_input == 1:
            self.test_object_traindatahandle.test_input_data()
        self.test_object_traindatahandle.test_search_data_key()
        self.test_object_traindatahandle.test_search_data_size()
        self.test_object_traindatahandle.test_search_data_range()
        self.test_object_traindatahandle.test_duplicate_avoid()
        self.test_object_traindatahandle.test_output_data()
        self.test_object_traindatahandle.test_initialization()
        self.test_object_traindatahandle.test_input_selected_data_to_selected_table()

# 测试数据库模块
class DatabaseHandleTest:
    test_object_databasehandle = DatabaseHandle()


if __name__ == "__main__":
    test = TrainDataHandleTest()
    test.test()
