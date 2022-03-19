# 定义DNN网络
from paddle import fluid


class MyDNN(fluid.dygraph.Layer):
    '''
    DNN网络
    '''

    def __init__(self):
        super(MyDNN, self).__init__()
        # 初始化

    def forward(self, input):
        # 前向传播
        # 定义网络结构
        # 定义第一层
        # 定义第二层
        # 定义第三层


# forward 定义执行实际运行时网络的执行逻辑