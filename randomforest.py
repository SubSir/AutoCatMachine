import numpy as np
from sklearn.ensemble import RandomForestRegressor
from joblib import dump


def main(x, y):

    x = np.array(x)  # 转换为NumPy数组
    y = np.array(y)  # 转换为NumPy数组
    rf_regressor = RandomForestRegressor(
        n_estimators=500, random_state=42
    )  # 例如，设置为500棵树
    rf_regressor.fit(x, y)
    dump(rf_regressor, "random_forest_model.joblib")


if __name__ == "__main__":
    # 假设x和y是适当格式的数据，例如：
    x = [[300750]]  # 示例特征数据，根据实际情况调整
    y = [20100620]  # 示例目标值，根据实际情况调整
    main(x, y)
