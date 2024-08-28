import os
import stock_hist_em as hist_em
from joblib import load
from datetime import datetime
import numpy as np
import csv


def main(long={}):
    stock_list = []
    items = os.listdir("models")
    for item in items:
        stock_list.append(item.split(".")[0])
    past_behavior = {}
    with open("benefit.csv", "r", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            past_behavior[row[0]] = float(row[1])
    try:
        for stock in stock_list:
            now = datetime.now()
            strdate = now.strftime("%Y%m%d")
            df = hist_em.stock_zh_a_hist(
                stock,
                "daily",
                "20240520",
                strdate,
            )
            df.drop(
                columns=["成交额", "振幅", "涨跌幅", "涨跌额", "换手率"], inplace=True
            )
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
            close = []
            tr = []
            flag = False
            for row in df.itertuples(index=True, name="Pandas"):
                xi = []
                if flag == False:
                    flag = True
                else:
                    tr.append(
                        max(
                            row[3] - row[4],
                            abs(close[-1] - row[3]),
                            abs(close[-1] - row[4]),
                        )
                    )
                for i in range(1, len(row[1:])):
                    xi.append(row[1:][i])
                    if i == 2:  # Close
                        close.append(row[1:][i])
                x.append(xi)
            wma = []
            for i in range(2, len(close)):
                wma.append((3 * close[i] + 2 * close[i - 1] + close[i - 2]) / 6)
            x = x[-1]
            x.append(wma[-1])
            loaded_model = load("models/" + stock + ".joblib")
            new_data = np.array([x])
            prediction = loaded_model.predict(new_data)
            prediction = wma[-1] + prediction[0]
            sma20 = np.mean(close[-20:])
            atr = np.mean(tr[-20:])
            stddev20 = np.std(close[-20:])
            upper_track = sma20 + 2 * stddev20
            lower_track = sma20 - 2 * stddev20
            if prediction <= lower_track:
                print(stock, "Buy, Past Benefit:", past_behavior[stock])

            if stock in long:
                if prediction >= upper_track or prediction < long[stock] - 3 * atr:
                    print(stock, "Sell")
    except:
        pass


if __name__ == "__main__":
    input_num = input("输入持仓数量")
    if input_num == "0":
        main()
    else:
        input_num = int(input_num)
        while input_num > 0:
            stock = input("输入持仓股票")
            buy_price = input("输入持仓价格")
            long = {}
            long[stock] = float(buy_price)
            input_num -= 1
        main(long)
