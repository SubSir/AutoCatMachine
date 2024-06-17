import pymysql
import pandas as pd

# 数据库连接配置
db_config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "123456",
    "db": "falc_pro",
    "charset": "utf8mb4",
}

# 连接到数据库
connection = pymysql.connect(**db_config)

# 读取满足条件的组
query_groups = """
SELECT DISTINCT 公司代码, 报告日期
FROM Financial_Data_With_Enough_Projects;
"""
groups_df = pd.read_sql(query_groups, connection)

# 初始化一个字典来存储每个项目编号出现的次数
project_counts = {}

# 遍历所有组
for index, row in groups_df.iterrows():
    company_code, report_date = row["公司代码"], row["报告日期"]

    # 对于每个组，查询对应的项目编号
    query_projects = f"""
    SELECT 项目编号
    FROM financial_data
    WHERE 公司代码 = '{company_code}' AND 报告日期 = '{report_date}';
    """
    projects_df = pd.read_sql(query_projects, connection)

    # 更新项目编号计数
    for project_code in projects_df["项目编号"]:
        if project_code in project_counts:
            project_counts[project_code] += 1
        else:
            project_counts[project_code] = 1

# 找出出现次数大于等于80的项目编号
common_project_codes = [code for code, count in project_counts.items() if count >= 1]

print("出现次数大于等于1的项目编号:", common_project_codes)

# 关闭数据库连接
connection.close()
