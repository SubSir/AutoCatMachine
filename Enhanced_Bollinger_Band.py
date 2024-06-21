import backtrader as bt
import pandas as pd
from datetime import datetime
from backtrader.feeds import GenericCSVData
import numpy as np

# 假设您已经训练了一个随机森林模型，可以预测下一个时间点的WMA值
# model = RandomForestRegressor(...)
# X_train, y_train = ... # 训练数据
# model.fit(X_train, y_train)


class MyCSVData(GenericCSVData):
    # 定义列名映射到Backtrader字段
    lines = ("Open", "Close", "High", "Low", "Volume")
    params = (
        ("dtformat", "%Y-%m-%d"),  # 日期格式
        ("Date", 0),  # 日期列索引
        ("Open", 1),  # 开盘价列索引
        ("Close", 2),  # 最高价列索引
        ("High", 3),  # 最低价列索引
        ("Low", 4),  # 收盘价列索引
        ("Volume", 5),  # 成交量列索引
        ("openinterest", -1),  # 开仓兴趣列索引，如果不存在可以设置为-1
    )


def main(predictions, date1, date2):

    def predict_wma(t):
        return predictions[t]  # 返回预测的WMA值

    # 自定义策略
    class MyStrategy(bt.Strategy):
        params = (("atr_multiplier", 3),)

        def __init__(self):
            self.sma20 = bt.indicators.SimpleMovingAverage(self.data.close, period=20)
            self.stddev20 = bt.indicators.StandardDeviation(self.data.close, period=20)
            self.upper_track = self.sma20 + 3 * self.stddev20  # 布林带上轨
            self.lower_track = self.sma20 - 3 * self.stddev20  # 布林带下轨
            self.atr = bt.indicators.ATR(period=20)
            self.buy_price = None
            self.position_type = None  # 用于记录仓位类型：None, 'long', 'short'

        def next(self):
            current_index = len(self.data) - 1
            predicted_wma = predict_wma(current_index)
            atr_value = self.params.atr_multiplier * self.atr[0]

            # 检查是否需要开仓
            if not self.position:
                if predicted_wma <= self.lower_track[0]:
                    self.buy_price = self.data.close[0]  # 初始化buy_price
                    self.buy(size=100)
                    self.position_type = "long"
                elif predicted_wma >= self.upper_track[0]:
                    self.buy_price = self.data.close[0]  # 初始化buy_price
                    self.sell(size=100)  # 卖空同等数量
                    self.position_type = "short"

            # 检查是否需要平仓，增加对None的检查
            if self.position_type == "long":
                if (
                    self.buy_price is None
                    or predicted_wma < self.buy_price - atr_value
                    or predicted_wma >= self.upper_track[0]
                ):
                    self.sell(size=self.position.size)
                    self.position_type = None
                    self.buy_price = None  # 平仓后重置buy_price

            elif self.position_type == "short":
                if (
                    self.buy_price is None
                    or predicted_wma > self.buy_price + atr_value
                    or predicted_wma <= self.lower_track[0]
                ):
                    self.buy(size=self.position.size)  # 平仓买入同等数量
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


if __name__ == "__main__":
    date1 = "20230101"
    date2 = "20230630"
    main("300750", date1, date2)
