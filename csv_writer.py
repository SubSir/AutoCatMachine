import pandas as pd

# 定义数据字典
data = {
    "公司代码": ["000001", "000002", "000003"],
    "报告日期": ["2023-01-01", "2023-01-02", "20000-01-03"],
    "收入_万元": [10000, 15000, 20000],
}

# 将字典转换为DataFrame
df = pd.DataFrame(data)

# 指定文件名
filename = "example_pandas.csv"

# 将DataFrame保存为CSV文件
df.to_csv(filename, index=False, encoding="utf-8-sig")
