import main
import pymysql
import csv
import os

config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "123456",
    "db": "instockdb",
    "charset": "utf8mb4",
}

# 目标字段列表
stock_list = []

try:
    # 创建连接
    connection = pymysql.connect(**config)

    # 创建游标
    with connection.cursor() as cursor:
        # 构建SQL查询语句，使用DISTINCT去除重复行，选取感兴趣的字段
        select_query = f"SELECT DISTINCT code FROM cn_stock_spot;"

        # 执行查询
        cursor.execute(select_query)
        # 获取所有数据
        results = cursor.fetchall()

        for row in results:
            stock_list.append(row)

finally:
    # 关闭连接
    if connection:
        connection.close()

for stock in stock_list:
    try:
        benefit = main.main(stock[0], "20120620", "20240620")
        with open("benefit.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([stock[0], benefit])
        if benefit <= 0:
            os.remove("models/" + stock[0] + ".joblib")
    except:
        pass
