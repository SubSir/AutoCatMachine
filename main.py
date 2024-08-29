import prepare
import Enhanced_Bollinger_Band
import stock_hist_em as hist_em
from joblib import load
from sklearn.ensemble import RandomForestRegressor
import randomforest
from datetime import datetime
import numpy as np

date1 = "20120620"
date2 = "20240620"
num = "300201"


def main(num, date1, date2):
    df = hist_em.stock_zh_a_hist(
        num,
        "daily",
        date1,
        date2,
    )
    df.drop(columns=["成交额", "振幅", "涨跌幅", "涨跌额", "换手率"], inplace=True)
    # 重命名列以匹配Backtrader的要求
    df.rename(
        columns={
            "日期": "Date",
            "开盘": "Open",
            "收盘": "Close",
            "最高": "High",
            "最低": "Low",
            "成交量": "Volume",
            # '成交额': 'Adj Close',  # 如果您想包含调整后的收盘价，取消注释并根据需要进行重命名
        },
        inplace=True,
    )
    x = []
    date = []
    close = []
    for row in df.itertuples(index=True, name="Pandas"):
        xi = []
        for i in range(len(row[1:])):
            if i == 0:
                date.append(row[1:][i])
            else:
                xi.append(row[1:][i])
            if i == 2:  # Close
                close.append(row[1:][i])
        x.append(xi)
    wma = []
    for i in range(2, len(close)):
        wma.append((3 * close[i] + 2 * close[i - 1] + close[i - 2]) / 6)
    x = x[2:]
    date = date[2:]
    for i in range(len(x)):
        x[i].append(wma[i])
    y = []
    for i in range(len(wma) - 1):
        y.append(wma[i + 1] - wma[i])

    train = int(len(x) * 0.8)
    randomforest.main(num, x[:train], y[:train])

    strd1 = date[train].replace("-", "")
    strd2 = date[-1].replace("-", "")

    prepare.main(num, strd1, strd2)

    # 加载模型
    loaded_model = load("models/" + num + ".joblib")

    # 假设我们有新的特征数据来预测
    new_data = np.array(x[train:])

    # 使用加载的模型进行预测
    prediction = loaded_model.predict(new_data)
    for i in range(len(prediction)):
        prediction[i] += wma[train + i]

    return Enhanced_Bollinger_Band.main(prediction, strd1, strd2)


if __name__ == "__main__":
    main(num, date1, date2)
