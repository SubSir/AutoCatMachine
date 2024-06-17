# 导入所需库
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import csv
import numpy as np

X = []
with open("X.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        X.append(tuple(float(i) for i in row))

y = []
with open("y.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        y.append(float(row[0]))

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
