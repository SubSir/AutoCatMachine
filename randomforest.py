# 导入所需库
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import pymysql
import numpy as np

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
    "BS-10",
    "BS-11",
    "BS-21",
    "BS-22",
    "BS-3",
    "BS-33",
    "BS-34",
    "BS-40",
    "BS-46",
    "BS-47",
    "BS-51",
    "BS-53",
    "BS-56",
    "BS-57",
    "BS-58",
    "BS-6",
    "BS-67",
    "BS-8",
    "BS-80",
    "BS-81",
    "BS-83",
    "BS-84",
    "BS-90",
    "BS-91",
    "BS-93",
    "BS-94",
    "CF-10",
    "CF-11",
    "CF-12",
    "CF-19",
    "CF-20",
    "CF-24",
    "CF-25",
    "CF-27",
    "CF-32",
    "CF-34",
    "CF-36",
    "CF-37",
    "CF-38",
    "CF-40",
    "CF-41",
    "CF-42",
    "CF-44",
    "CF-47",
    "CF-48",
    "CF-5",
    "CF-58",
    "CF-6",
    "CF-63",
    "CF-64",
    "CF-68",
    "CF-7",
    "CF-72",
    "CF-73",
    "CF-76",
    "CF-8",
    "CF-9",
    "PS-10",
    "PS-16",
    "PS-17",
    "PS-18",
    "PS-2",
    "PS-20",
    "PS-22",
    "PS-23",
    "PS-26",
    "PS-27",
    "PS-29",
    "PS-3",
    "PS-4",
    "PS-5",
    "PS-6",
    "PS-7",
    "PS-8",
    "PS-9",
]

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
        select_query = f"SELECT DISTINCT {', '.join(fields_of_interest)} FROM corporation_information;"

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

X = []
y = []
corporation = ""
corporation_info = []
for item in data_list:
    if item[0] != corporation:
        corporation_info = []
        corporation_info += corporations_info[item[0]]
        corporation_info += issues_info[item[0]]
        corporation = item[0]

X = np.array(X)
y = np.array(y)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 初始化随机森林分类器
rf_clf = RandomForestClassifier(
    n_estimators=100, max_depth=10, random_state=42  # 决策树的数量  # 树的最大深度
)  # 设置随机种子以确保结果的可复现性

# 训练模型
rf_clf.fit(X_train, y_train)

# 预测测试集
y_pred = rf_clf.predict(X_test)

# 评估模型
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)

# 可视化特征重要性（可选）
import matplotlib.pyplot as plt

importances = rf_clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in rf_clf.estimators_], axis=0)
indices = np.argsort(importances)[::-1]

plt.figure()
plt.title("Feature importances")
plt.bar(
    range(X.shape[1]),
    importances[indices],
    color="r",
    yerr=std[indices],
    align="center",
)
plt.xticks(range(X.shape[1]), [X.columns[i] for i in indices], rotation=90)
plt.xlim([-1, X.shape[1]])
plt.show()
