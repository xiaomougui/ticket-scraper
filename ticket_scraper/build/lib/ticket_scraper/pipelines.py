# import sqlite3
#
# class TicketScraperPipeline:
#     def open_spider(self, spider):
#         self.connection = sqlite3.connect("tickets.db")
#         self.cursor = self.connection.cursor()
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS tickets(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 event_name TEXT,
#                 event_date TEXT,
#                 event_location TEXT,
#                 ticket_price TEXT
#             )
#         ''')
#         self.connection.commit()
#
#     def close_spider(self, spider):
#         self.connection.close()
#
#     def process_item(self, item, spider):
#         self.cursor.execute('''
#             INSERT INTO tickets (event_name, event_date, event_location, ticket_price) VALUES (?, ?, ?, ?)
#         ''', (item['event_name'], item['event_date'], item['event_location'], item['ticket_price']))
#         self.connection.commit()
#         return item
#

import csv
import pymysql
# from scrapy.exceptions import NotConfigured
# from scrapy import signals
# from myproject import settings



# 保存csv
class TicketPipeline:
    def __init__(self):
        # headers = ('票名', '时间','地点','价格','最低价','最高价','类别')
        headers = ('name','date', 'actors','location','location_details','price','lowPrice','highPrice','categoryName')
        self.f = open('ticket.csv', 'w+', encoding='utf-8', newline='')
        print(self.f,6666)
        self.f_csv = csv.DictWriter(self.f, headers)
        self.f_csv.writeheader()  # 写入表头

    def process_item(self, item, spider):
        self.f_csv.writerow(item)
        return item

    def close_spider(self, spider):
        self.f.close()
        print('ticket.csv文件写入完成')


# 保存Mysql
class MysqlTicketPipeline:
    def __init__(self):
        # 创建链接
        self.db = pymysql.Connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="hrn77799.",
            db="ticket-data"
        )
        # 创建游标，用于传递python给MySQL的命令和MySQL返回的内容
        self.cursor = self.db.cursor()

        # 不想手动创建数据库，也可以在init方法中实现
        sql_1 = """
            CREATE TABLE IF NOT EXISTS tickets(
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(255) not null,
                `date` VARCHAR(255) not null,
                `actors` VARCHAR(255) null,
                `location` VARCHAR(255) not null,
                `location_details` VARCHAR(255) null,
                `price` VARCHAR(255) null,
                `lowPrice` FLOAT null,
                `highPrice` FLOAT null,
                `categoryName` VARCHAR(255) null
                
            )
                """
        self.cursor.execute(sql_1)

    def process_item(self, item, spider):
        # SQL插入语句
        sql = "insert into tickets (`name`, `date`, `actors`, `location`, `location_details`, `price`, `lowPrice`, `highPrice`, `categoryName`) " \
              "values (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        # 执行SQL语句
        self.cursor.execute(sql,(item['name'],item['date'], item['actors'],item['location'],item['location_details'],item['price'],item['lowPrice'],item['highPrice'],item['categoryName']))  # 放值
        # 提交到数据库执行
        self.db.commit()
        return item

    def close_spider(self, spider):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.db.close()
        print('Mysql文件写入完成')
