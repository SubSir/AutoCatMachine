import stock_hist_em as hist_em
import numpy as np
import pymysql

# 数据库连接配置
config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "123456",
    "db": "financial_analysis_for_listed_companies",
    "charset": "utf8mb4",
}

# 目标字段列表
fields_of_interest = ["公司代码", "报告日期"]

try:
    # 创建连接
    connection = pymysql.connect(**config)

    # 创建游标
    with connection.cursor() as cursor:
        # 构建SQL查询语句，选取感兴趣的字段
        select_query = f"SELECT {', '.join(fields_of_interest)} FROM revenue_data;"

        # 执行查询
        cursor.execute(select_query)

        # 获取所有数据
        results = cursor.fetchall()

        # 将查询结果存储为列表
        data_list = [row for row in results]

finally:
    # 关闭连接
    if connection:
        connection.close()

print(data_list)


def sava_data_to_database(date_table):
    """保存数据至数据库

    创建数据库连接，打开数据库，并调用函数将数据存入 MySQL 数据库

    参数
    ----------
    date_table: list
        欲存入数据库的数据

    返回值
    -------
    无
    """

    """ 创建数据库连接及游标 """
    DB = pymysql.connect(
        host="127.0.0.1", port=3306, user="root", passwd="123456", db="consequence_db"
    )
    cursor = DB.cursor()

    """ 将数据写入数据库 """
    print("开始向数据库写入数据...")
    table_name = "consequence_db"
    fileds = "公司代码, 日期, 值"
    field_values = r"%s, %s, %s"

    cursor.executemany(
        f"INSERT INTO { table_name }({ fileds }) VALUES ({ field_values })",
        date_table,
    )

    """ 向数据库提交操作并关闭数据库连接 """
    DB.commit()
    DB.close()

    print("数据保存成功！")

    return


df = hist_em.stock_zh_a_hist(
    "000001",
    "daily",
    "20210229",
    "20220229",
)
# 假设你的数据存储在df中
data = df.values

print(df)
