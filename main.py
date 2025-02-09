# @Time : 2020/5/8 11:13

# @Author : songshangru

# @File : main.py

# @Software: PyCharm
import pymysql
import conf
import time
import os
import shutil
from core.data_parse import DataParse


class TrainDataHandle:
    def __init__(self):
        self.host = conf.DATABASE_CONNECT_INFORMATION['host']
        self.user = conf.DATABASE_CONNECT_INFORMATION['user']
        self.password = conf.DATABASE_CONNECT_INFORMATION['password']
        self.port = int(conf.DATABASE_CONNECT_INFORMATION['port'])  # 端口应该接收整形
        self.db = conf.DATABASE_CONNECT_INFORMATION['db']

        # 连接数据库
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db)
        self.cursor = self.conn.cursor()

    # 获得数据表的属性字段
    def get_fields(self, table_name):
        # 构造sql语句
        sql = "select * from " + table_name + ' limit 1'
        # 执行查询
        self.cursor.execute(sql)
        desc = self.cursor.description

        # 转换格式
        fields = []
        for field in desc:
            # 去除id,之所以时field[0],是因为执行结果desc显示的是机构信息，每一个字段一个列表，而名字为列表第一个
            if field[0] == 'id':
                continue
            fields.append(field[0])
        return fields

    # 构造sql语句
    # 1为插入语句
    # 2为联表查询语句
    # 3为删除语句
    def construct_sql(self, table_name, sql_type):
        sql = ''
        # 用于构造查询语句中的选中表部分
        select_fields = self.get_fields(table_name=conf.TABLE['DATA_SELECT'])

        if sql_type == 1:
            all_fields = self.get_fields(table_name)

            # 构造属性部分
            inserted_field = ''
            for field in all_fields:
                inserted_field += '`' + field + '`, '
            # 去除最后一个逗号
            inserted_field = inserted_field[:-2]

            # 构造插入函数的通用部分
            sql = "INSERT INTO " + '`' + conf.DATABASE_CONNECT_INFORMATION[
                'db'] + '`' + "." + '`' + table_name + '` ' + '(' + inserted_field + ')' + ' VALUES '

        elif sql_type == 2:
            # 构造查询函数的通用部分
            sql = "SELECT " + table_name + ".* FROM " + table_name + " LEFT JOIN " + conf.TABLE['DATA_SELECT'] +\
                  " ON " + table_name + ".id = " + conf.TABLE['DATA_SELECT'] + "." + select_fields[0] + " WHERE " +\
                  conf.TABLE['DATA_SELECT'] + "." + select_fields[0] + " IS NULL AND "

        elif sql_type == 3:
            # 主要用于初始化选中表
            sql = 'delete from ' + conf.TABLE['DATA_SELECT']

        return sql

    # 输入需要解析的记录文件，如excel，csv等格式
    # file为记录文件的绝对路径加文件名
    def input_data(self, table_name=conf.TABLE['DATA_INFORMATION'], contents=''):
        # 若没内容，则传入训练数据
        if contents == '':
            contents = DataParse().parse_csv(output_type=1)
        # 获得需要写入的字段
        fields = self.get_fields(table_name)

        # 构造sql语句
        sql = self.construct_sql(table_name=table_name, sql_type=1)

        print('开始构造sql语句')
        for row in contents:
            # 构造数据，一次构造出需要插入的所有数据
            inserted_value = '('
            # 添加原生属性
            for i in range(len(fields)):
                if fields[i] == 'select_time' or fields[i] == 'create_time':
                    inserted_value += '\'' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\', '
                else:
                    if isinstance(row, int):
                        inserted_value += '\'' + str(row) + '\', '
                    else:
                        inserted_value += '\'' + str(row[i]) + '\', '
            inserted_value = inserted_value[:-2] + '), '

            # 与通用部分进行拼接
            sql += str(inserted_value)
        sql = sql[:-2] + ';'  # 加上[:-2]是为了去除尾部多余的逗号

        print("开始插入")
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print("插入失败")

    # 按关键字查询
    # if_like为1是模糊查询，0是非模糊查询
    # field为查询字段
    # key_word为查询关键字
    # nums 为查询数量
    def search_data_key(self, field, key_word, nums=1, if_like=0):
        if nums < 0:
            print("搜索数量不能小于0")
            return False
        if field is None:
            print("给出字段不能为空")
            return False
        if key_word is None:
            print("搜索关键字不能为空")
            return False

        sql = self.construct_sql(table_name=conf.TABLE['DATA_INFORMATION'], sql_type=2)

        # 判断是否需要进行模糊查询
        if if_like == 0:
            sql += conf.TABLE['DATA_INFORMATION'] + "." + field + " = %s LIMIT %s;"
            self.cursor.execute(sql, [str(key_word), nums])
        elif if_like == 1:
            key_word_1 = '%|' + str(key_word) + '%'
            key_word_2 = '%' + str(key_word) + '|%'
            sql += conf.TABLE['DATA_INFORMATION'] + "." + field + " LIKE %s or " + field + " LIKE %s " + "LIMIT %s"

            self.cursor.execute(sql, [key_word_1, key_word_2, nums])
        else:
            print("没有你要的查询类型")
            return False

        results = self.cursor.fetchall()

        # 判断结果是否为空
        if not results:
            print("没有查询到任何不重复数据")
            return False

        return results

    # 按大小查询
    # field为查询字段
    # key_word为查询关键字
    # nums 为查询数量
    # com_type = 1  大于
    # com_type = 2  大于等于
    # com_type = 3  小于
    # com_type = 4  小于等于
    def search_data_size(self, field, key_word, nums=1, com_type='>'):
        if nums < 0:
            print("搜索数量不能小于0")
            return False
        if field is None:
            print("给出字段不能为空")
            return False
        if key_word is None:
            print("搜索关键字不能为空")
            return False

        sql = self.construct_sql(table_name=conf.TABLE['DATA_INFORMATION'], sql_type=2)

        # 判断比较类型是否合法
        if com_type not in ['>', '>=', '<', '<=']:
            print("这里没有你想要的东西")
            return False

        sql += conf.TABLE['DATA_INFORMATION'] + "." + field + " " + com_type + " %s LIMIT %s"

        self.cursor.execute(sql, [key_word, nums])
        results = self.cursor.fetchall()

        # 判断结果是否为空
        if not results:
            print("没有查询到任何不重复数据")
            return False

        return results

    # 按范围查询
    # field为查询字段
    # key_word_1,key_word_2为查询关键字
    # nums 为查询数量
    def search_data_range(self, field, key_word_1, key_word_2, nums=1):
        if nums < 0:
            print("搜索数量不能小于0")
            return False
        if field is None:
            print("给出字段不能为空")
            return False
        if key_word_1 is None and key_word_2 is None:
            print("搜索关键字不能为空")
            return False

        # 构造
        sql = self.construct_sql(table_name=conf.TABLE['DATA_INFORMATION'], sql_type=2)
        sql += conf.TABLE['DATA_INFORMATION'] + "." + field + " BETWEEN %s and %s LIMIT %s"

        # 查询
        self.cursor.execute(sql, [key_word_1, key_word_2, nums])
        results = self.cursor.fetchall()

        if not results:
            print("没有查询到任何不重复数据")
            return False

        return results

    # 避免重复，通过将查询出的结果插入到选中表中，下一次进行联表查询时会自动去除已有结果
    def duplicate_avoid(self, results):
        if results is None:
            return False

        # 通过将查询结果插入到选中表来防止选中错误
        self.input_data(table_name=conf.TABLE['DATA_SELECT'], contents=results)

    # 如果dup_tag = 0，则为不重复选取
    def output_data(self, data_sets, if_dup=0):
        if not data_sets:
            print("没有任何输出结果")
            return False

        output_dir = conf.PATH['DATA_OUTPUT']
        data_dir = conf.PATH['DATA']
        indexs = []

        if if_dup == 0:
            self.duplicate_avoid(data_sets)

        for data in data_sets:
            indexs.append(data[1])

        for files in os.listdir(data_dir):
            if files in indexs:
                file_dir = output_dir + "\\" + files
                files = data_dir + "\\" + files
                shutil.copy(files, file_dir)
                print(files + "已被复制")

    # 初始化选取，从零开始
    def initialization(self):
        # 清空选中表
        sql = self.construct_sql(table_name=conf.TABLE['DATA_SELECT'], sql_type=3)

        self.cursor.execute(sql)
        self.conn.commit()

        # 清空输出文件夹
        for i in os.listdir(conf.PATH['DATA_OUTPUT']):
            file = conf.PATH['DATA_OUTPUT'] + '\\' + i
            os.remove(file)
        print('初始化成功')

    # 导入已选数据到选中表,需要根据需要数据名称在数据库中查询该数据是否存在，若存在，则取其id，作为选中表的data_id导入
    # 需要导入的数据放在outputs文件夹
    def input_selected_data_to_selected_table(self):
        # 读取指定文件夹，取得数据名字
        file_name_sets = []
        selected_file_input_path = conf.PATH['DATA_OUTPUT']
        for i in os.walk(selected_file_input_path):
            file_name_sets = i[2]

        # 查询数据名字是否在主数据表中，若不在，则将其标记并打印提示用户，若在，则将其id存储，并进行下一步
        data_information_fields = self.get_fields(conf.TABLE['DATA_INFORMATION'])
        select_data_fields = self.get_fields(conf.TABLE['DATA_SELECT'])

        file_id_sets = []
        for i in file_name_sets:
            sql = "SELECT id FROM " + conf.TABLE['DATA_INFORMATION'] + " WHERE " + data_information_fields[0] + " = '%s'" % i
            self.cursor.execute(sql)
            search_result = self.cursor.fetchone()

            if search_result is None:
                print("数据:" + str(i) + "不在数据集中")
            else:
                file_id_sets.append(search_result[0])

        # 查询数据id是否在选中表中，若在，则忽略，若不在，则加入用于插入的列表，则进行下一步
        file_id_need_input = []
        for i in file_id_sets:
            sql = "SELECT id FROM " + conf.TABLE['DATA_SELECT'] + " WHERE " + select_data_fields[
                0] + " = '%s'" % i

            self.cursor.execute(sql)
            search_result = self.cursor.fetchone()

            if search_result is None:
                file_id_need_input.append(i)

        # 根据用于插入的列表中存储的主表id，将其作为选中表的外键id插入选中表
        if file_id_need_input:
            self.duplicate_avoid(file_id_need_input)
            print("已将数据加入选中表")
        else:
            print("所有数据都已在选中表")

    # 完成后自动关闭数据库和游标
    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    start_time = int(time.time())
    # 测试区域
    f = TrainDataHandle()

    # result = f.get_fields(table_name=conf.TABLE['DATA_SELECT'])
    result = f.search_data_key(field='finding_labels', key_word='Mass', nums=50, if_like=1)
    # f.out_put_data(data_sets=result)
    # f.initialization()
    # f.input_selected_data_to_selected_table()

    # f.initialization()

    print(result)

    end_time = int(time.time())
    use_time = end_time - start_time
    print("耗时" + str(use_time) + "秒")
