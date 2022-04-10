# 定义DNN网络
import paddle
class MyDNN(paddle.nn.Layer):
    def __init__(self):
        super(MyDNN, self).__init__()
        self.linear1 = paddle.nn.Linear(in_features=3 * 224 * 224, out_features=1024)
        self.relu1 = paddle.nn.ReLU()

        self.linear2 = paddle.nn.Linear(in_features=1024, out_features=512)
        self.relu2 = paddle.nn.ReLU()

        self.linear3 = paddle.nn.Linear(in_features=512, out_features=128)
        self.relu3 = paddle.nn.ReLU()

        self.linear4 = paddle.nn.Linear(in_features=128, out_features=25)
        self.relu4 = paddle.nn.LogSoftmax()

        # self.fc1 = paddle.fluid.dygraph.Linear(input_dim=28*28, output_dim=100, act='relu')

    def forward(self, input):  # forward 定义执行实际运行时网络的执行逻辑
        # input.shape (16, 3, 224, 224)
        x = paddle.reshape(input, shape=[-1, 3 * 224 * 224])  # -1 表示这个维度的值是从x的元素总数和剩余维度推断出来的，有且只能有一个维度设置为-1
        # print(x.shape)
        x = self.linear1(x)
        x = self.relu1(x)
        # print('1', x.shape)
        x = self.linear2(x)
        x = self.relu2(x)
        # print('2',x.shape)
        x = self.linear3(x)
        x = self.relu3(x)
        # print('3',x.shape)
        y = self.linear4(x)
        # print('4',y.shape)
        y = self.relu4(y)
        return y