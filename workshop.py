# 导入所需库
import csv
import pymysql
from datetime import datetime

date_list = [
    "2019-06-30",
    "2019-09-30",
    "2019-12-31",
    "2020-03-31",
    "2020-06-30",
    "2020-09-30",
    "2020-12-31",
    "2021-03-31",
    "2021-06-30",
    "2021-09-30",
    "2021-12-31",
    "2022-03-31",
    "2022-06-30",
    "2022-09-30",
    "2022-12-31",
    "2023-03-31",
    "2023-06-30",
    "2023-09-30",
    "2023-12-31",
    "2024-03-31",
]

index_list = [
    "PS-22",
    "PS-23",
    "PS-20",
    "PS-16",
    "PS-2",
    "CF-12",
    "CF-40",
    "PS-3",
    "CF-25",
    "CF-38",
    "PS-4",
    "PS-5",
    "CF-42",
    "PS-8",
    "CF-11",
    "CF-6",
    "CF-37",
    "CF-24",
    "PS-9",
    "CF-32",
    "CF-41",
    "CF-5",
    "CF-8",
    "CF-10",
    "CF-19",
    "CF-9",
    "PS-7",
    "BS-47",
    "BS-93",
    "BS-94",
    "CF-7",
    "CF-20",
    "CF-3",
    "BS-91",
    "BS-81",
    "PS-6",
    "PS-29",
    "PS-21",
    "PS-26",
    "BS-67",
    "BS-22",
    "BS-46",
    "BS-80",
    "BS-3",
    "BS-83",
    "BS-90",
    "BS-10",
    "BS-57",
    "BS-56",
    "BS-84",
    "BS-16",
    "BS-53",
    "PS-18",
    "BS-40",
    "PS-30",
    "BS-8",
    "PS-17",
    "PS-27",
    "BS-44",
    "PS-10",
    "BS-21",
]
index_list_str = "','".join(
    index_list
)  # 将列表转换为逗号分隔的字符串，每个元素都被单引号包裹

# 数据库连接配置
config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "123456",
    "db": "consequence_db",
    "charset": "utf8mb4",
}


try:
    # 创建连接
    connection = pymysql.connect(**config)

    # 创建游标
    with connection.cursor() as cursor:
        # 构建SQL查询语句，使用DISTINCT去除重复行，选取感兴趣的字段
        select_query = f"SELECT * FROM consequence_data;"

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

config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "123456",
    "db": "falc_pro",
    "charset": "utf8mb4",
}

# 目标字段列表
fields_of_interest = ["公司代码", "发行价格", "注册资本"]
corporations_info = {}

try:
    # 创建连接
    connection = pymysql.connect(**config)

    # 创建游标
    with connection.cursor() as cursor:
        # 构建SQL查询语句，使用DISTINCT去除重复行，选取感兴趣的字段
        select_query = f"SELECT DISTINCT {', '.join(fields_of_interest)} FROM corporation_information;"

        # 执行查询
        cursor.execute(select_query)
        # 获取所有数据
        results = cursor.fetchall()

        for row in results:
            corporations_info[row[0]] = [row[1], row[2]]

finally:
    # 关闭连接
    if connection:
        connection.close()

# 目标字段列表
fields_of_interest = [
    "公司代码",
    "每股发行价",
    "首发前总股本",
    "首发后总股本",
    "实际发行量",
    "实际募集资金合计",
    "发行费用总额",
    "募集资金净额",
    "承销费用",
]
issues_info = {}

try:
    # 创建连接
    connection = pymysql.connect(**config)

    # 创建游标
    with connection.cursor() as cursor:
        # 构建SQL查询语句，使用DISTINCT去除重复行，选取感兴趣的字段
        select_query = (
            f"SELECT DISTINCT {', '.join(fields_of_interest)} FROM issue_information;"
        )

        # 执行查询
        cursor.execute(select_query)
        # 获取所有数据
        results = cursor.fetchall()

        for row in results:
            issues_info[row[0]] = [
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
            ]

finally:
    # 关闭连接
    if connection:
        connection.close()


def fetch_finance_data(corporation, date):
    fields_of_interest = "值"
    try:
        # 创建连接
        connection = pymysql.connect(**config)

        # 创建游标
        with connection.cursor() as cursor:
            # 构建SQL查询语句，使用DISTINCT去除重复行，选取感兴趣的字段
            select_query = f"SELECT {fields_of_interest} FROM financial_data WHERE 公司代码 = '{corporation}' AND 报告日期 = '{date}' AND 项目编号 IN ('{index_list_str}');"

            # 执行查询
            cursor.execute(select_query)
            # 获取所有数据
            results = cursor.fetchall()

    finally:
        # 关闭连接
        if connection:
            connection.close()
    return [row[0] for row in results]


X = []
y = []
problem_list = []
corporation = ""
corporation_info = []
cnt = 0
for item in data_list:
    if item[0] not in corporations_info:
        continue
    if item[0] not in issues_info:
        continue
    if item[0] != corporation:
        corporation_info = corporations_info[item[0]]
        corporation_info += issues_info[item[0]]
        corporation = item[0]
    date = date_list.index(item[1])
    if date == 0:
        continue
    date -= 1
    pre_item = item
    for item2 in data_list:
        if item2[0] == item[0] and item2[1] == date_list[date]:
            pre_item = item2
            break
    iy = round((item[2] - item2[2]) / item2[2], 2)

    date_format = "%Y-%m-%d"

    # 使用strptime将字符串转换为date对象
    date_obj = datetime.strptime(date_list[date], date_format).date()

    fet = fetch_finance_data(item[0], date_obj)
    if len(fet) < len(index_list):
        continue
    ix = corporation_info + fet + [item2[2]]
    X.append(ix)
    y.append(iy)
    cnt += 1
    print(str(cnt / len(data_list) * 100) + "% 已完成 收入了" + str(len(y)) + "条信息")

# 存储 X
with open("X.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(X)

# 存储 y
with open("y.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for val in y:
        writer.writerow([val])
