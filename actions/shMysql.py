# import pymysql
#
# class ShMysql:
#
#     def __init__(self):
#         # 创建一个连接数据库的对象
#         self.conn = pymysql.connect(
#             host='127.0.0.1',  # 连接的数据库服务器主机名
#             port=3306,  # 数据库端口号
#             user='root',  # 数据库登录用户名
#             passwd='123456',
#             db='mysql',  # 数据库名称
#             charset='utf8',  # 连接编码
#         )
#         # 使用cursor()方法创建一个游标对象，用于操作数据库
#         self.cur = self.conn.cursor()
#
#     def op(self):
#         self.cur.execute("select * from shop.department")
#         result = self.cur.fetchone()  # 使用 fetchone()方法获取单条数据.只显示一行结果
#         return result
#
#     def run(self):
#         self.op()
#         print(self.op())
#         print("查询语句成功")
#
#
# if __name__ == '__main__':
#     ShMysql().run()
