import backtrader as bt
import pandas as pd
from datetime import datetime
from backtrader.feeds import GenericCSVData
import numpy as np


# 定义自定义数据类
class MyCSVData(GenericCSVData):
    # 定义列名映射到Backtrader字段
    lines = ("datetime", "open", "close", "high", "low", "volume")
    params = (
        ("dtformat", "%Y-%m-%d"),  # 日期格式
        ("datetime", 0),  # 日期列索引
        ("open", 1),  # 开盘价列索引
        ("close", 2),  # 收盘价列索引
        ("high", 3),  # 最高价列索引
        ("low", 4),  # 最低价列索引
        ("volume", 5),  # 成交量列索引
        ("openinterest", -1),  # 开仓兴趣列索引，如果不存在可以设置为-1
    )


def main(predictions, date1, date2, leverage_factor=2):

    def predict_wma(t):
        return predictions[t]  # 返回预测的WMA值

    # 自定义策略
    class MyStrategy(bt.Strategy):
        params = (("atr_multiplier", 3), ("leverage_factor", leverage_factor))

        def __init__(self):
            self.sma20 = bt.indicators.SimpleMovingAverage(self.data.close, period=20)
            self.stddev20 = bt.indicators.StandardDeviation(self.data.close, period=20)
            self.upper_track = self.sma20 + 2 * self.stddev20  # 布林带上轨
            self.lower_track = self.sma20 - 2 * self.stddev20  # 布林带下轨
            self.atr = bt.indicators.ATR(period=20)
            self.buy_price = None
            self.position_type = None  # 用于记录仓位类型：None, 'long', 'short'

        def next(self):
            current_index = len(self.data) - 1
            predicted_wma = predict_wma(current_index)
            atr_value = self.params.atr_multiplier * self.atr[0]
            leverage = (
                self.broker.getcash() * self.params.leverage_factor / self.data.close[0]
            )  # 计算可利用杠杆

            # 动态调整买入的大小，但需确保不超过可用资金
            size = min(int(leverage), self.broker.getcash() // self.data.close[0])

            # 检查是否需要开仓
            if not self.position:
                if predicted_wma <= self.lower_track[0]:
                    self.buy_price = self.data.close[0]  # 初始化buy_price
                    self.buy(size=size)
                    self.position_type = "long"

            # 检查是否需要平仓，增加对None的检查
            if self.position_type == "long":
                if (
                    self.buy_price is None
                    or predicted_wma < self.buy_price - 3 * atr_value
                    or predicted_wma >= self.upper_track[0]
                ):
                    self.sell(size=self.position.size)
                    self.position_type = None
                    self.buy_price = None  # 平仓后重置buy_price

    cerebro = bt.Cerebro()

    date_format = "%Y%m%d"
    from_date = datetime.strptime(date1, date_format)
    to_date = datetime.strptime(date2, date_format)

    # 加载数据
    data = MyCSVData(
        dataname="stock_data.csv",
        fromdate=from_date,
        todate=to_date,
    )

    # 添加数据到回测引擎
    cerebro.adddata(data)

    # 添加策略
    cerebro.addstrategy(MyStrategy)

    # 设置初始资金
    start_cash = 100000.0
    cerebro.broker.setcash(start_cash)

    # 运行回测
    cerebro.run()

    # 获取回测结束后的总资金
    end_cash = cerebro.broker.getvalue()

    # 计算总收益率
    total_return_percentage = ((end_cash - start_cash) / start_cash) * 100

    # 假设回测周期是从date1到date2，计算总天数
    total_days = (to_date - from_date).days
    # 假设一年有365天，计算平均年化收益率
    annualized_return_percentage = (
        (1 + total_return_percentage / 100) ** (365 / total_days)
    ) - 1
    annualized_return_percentage *= 100  # 转换为百分比形式

    # 打印最终的资产价值、总收益率和平均年化收益率
    print(f"Final Portfolio Value: {end_cash:.2f}")
    print(f"Total Return Percentage: {total_return_percentage:.2f}%")
    print(f"Average Annualized Return Percentage: {annualized_return_percentage:.2f}%")

    cerebro.plot()
    return annualized_return_percentage


if __name__ == "__main__":
    date1 = "20230101"
    date2 = "20230630"
    main("300750", date1, date2)
