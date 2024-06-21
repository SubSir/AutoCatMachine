import torch
import csv
import torch.nn as nn
import torch.optim as optim

# 数据加载
X = []
with open("X.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        row_ = []
        for k in range(10, len(row) - 1):
            row_.append(float(row[k]) / float(row[5]) / float(row[-1]))
        X.append(tuple(float(i) for i in row_))

y = []
with open("y.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        y.append(float(row[0]))

## 定义网络结构
input_size = 61  # 每个样本有72个特征
hidden_size = 64  # 你可以根据需要调整隐藏层的大小
output_size = 1  # 输出层大小为1，现在对应连续值预测


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)  # 第一层全连接层
        self.fc2 = nn.Linear(
            hidden_size, output_size
        )  # 第二层全连接层，无激活函数，直接输出连续值

    def forward(self, x):
        x = torch.relu(self.fc1(x))  # 使用ReLU激活函数
        x = self.fc2(x)  # 直接输出连续值
        return x


# 数据转换为PyTorch张量
X = torch.tensor(X, dtype=torch.float32)  # 直接转换为浮点型张量
y = torch.tensor(y, dtype=torch.float32)  # y已经是连续值，不需要unsqueeze

# 实例化网络、优化器和损失函数
net = Net()
optimizer = optim.SGD(net.parameters(), lr=0.01)
criterion = nn.MSELoss()  # 改为均方误差损失，适用于回归任务

# 训练循环
batch_size = 32
num_batches = len(X) // batch_size

for epoch in range(1000):
    running_loss = 0.0

    for batch in range(num_batches):
        start = batch * batch_size
        end = start + batch_size

        optimizer.zero_grad()
        outputs = net(X[start:end])
        loss = criterion(
            outputs.squeeze(), y[start:end]
        )  # 使用MSE损失，squeeze()用于去除输出的单维批次大小维度
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    if epoch % 100 == 99:
        print(f"Epoch {epoch+1}, Loss: {running_loss/num_batches}")

print("Training finished!")
torch.save(net.state_dict(), "model.pth")
