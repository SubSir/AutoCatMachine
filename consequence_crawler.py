import stock_hist_em as hist_em
import pymysql
from datetime import timedelta

# 数据库连接配置
config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "123456",
    "db": "falc_pro",
    "charset": "utf8mb4",
}

# 目标字段列表
fields_of_interest = ["公司代码", "报告日期"]

try:
    # 创建连接
    connection = pymysql.connect(**config)

    # 创建游标
    with connection.cursor() as cursor:
        # 构建SQL查询语句，使用DISTINCT去除重复行，选取感兴趣的字段
        select_query = (
            f"SELECT DISTINCT {', '.join(fields_of_interest)} FROM financial_data;"
        )

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
    table_name = "consequence_data"
    fileds = "公司代码, 日期, 值"
    field_values = r"%s, %s, %s"

    cursor.executemany(
        f"INSERT INTO { table_name }({ fileds }) VALUES ({ field_values }) ON DUPLICATE KEY UPDATE 值 = VALUES(值)",
        date_table,
    )

    """ 向数据库提交操作并关闭数据库连接 """
    DB.commit()
    DB.close()

    print("数据保存成功！")

    return


corporation = ""
consequence_list = []
for item in data_list:
    if corporation != item[0]:
        if corporation != "":
            sava_data_to_database(consequence_list)
            consequence_list = []
            print(corporation + "保存成功！")
        corporation = item[0]
    date = item[1]
    formatted_date = item[1].strftime("%Y%m%d")
    try:
        df = hist_em.stock_zh_a_hist(
            item[0],
            "daily",
            formatted_date,
            formatted_date,
        )
    except:
        continue
    if df.empty:
        date2 = date + timedelta(days=60)
        formatted_date2 = date2.strftime("%Y%m%d")
        try:
            df2 = hist_em.stock_zh_a_hist(
                item[0],
                "daily",
                formatted_date,
                formatted_date2,
            )
        except:
            continue
        if df2.empty:
            continue
    bl = False
    while df.empty:
        date += timedelta(days=1)
        formatted_date = date.strftime("%Y%m%d")
        try:
            df = hist_em.stock_zh_a_hist(
                item[0],
                "daily",
                formatted_date,
                formatted_date,
            )
        except:
            bl = True
            break
    if bl:
        continue
    consequence_list.append((item[0], item[1], df["开盘"][0]))

sava_data_to_database(consequence_list)
consequence_list = []
print(corporation + "保存成功！")
print("数据保存成功！")
