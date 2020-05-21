# @Time : 2020/5/20 11:46 

# @Author : songshangru

# @File : database.py

# @Software: PyCharm
import conf
import pymysql

class DatabaseHandle():
    def __init__(self):
        """
        构造函数，从conf导入连接配置，并连接数据库，返回连接对象和游标对象
        """
        self.host = conf.DATABASE_CONNECT_INFORMATION['host']
        self.user = conf.DATABASE_CONNECT_INFORMATION['user']
        self.password = conf.DATABASE_CONNECT_INFORMATION['password']
        self.port = int(conf.DATABASE_CONNECT_INFORMATION['port'])  # 端口应该接收整形
        self.db = conf.DATABASE_CONNECT_INFORMATION['db']

        # 连接数据库
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db)
        self.cursor = self.conn.cursor()


    """
    增
    """
    """
    删
    """
    """
    改
    """
    """
    查
    """


    def __del__(self):
        """
        析构函数，类关闭后，关闭连接和游标
        """
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    pass
