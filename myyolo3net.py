import paddle.fluid as fluid
# from paddle.fluid.initializer import MSRA
from paddle.fluid.param_attr import ParamAttr
from paddle.fluid.regularizer import L2Decay

def SmallConvBlock(inputL,num_filter,filter_size,act=None,stride=1):
    conv0 = fluid.layers.conv2d(
        input=inputL,
        num_filters=num_filter,
        filter_size=filter_size,
        stride=stride,
        act=None,
        padding="SAME",
        param_attr=ParamAttr(initializer=fluid.initializer.Normal(0., 0.02)),
        bias_attr=False
    )

    conv0_norm = fluid.layers.batch_norm(
        input=conv0,
        act=None,
        param_attr=ParamAttr(initializer=fluid.initializer.Normal(0., 0.02),regularizer=L2Decay(0.)),
        bias_attr=ParamAttr(initializer=fluid.initializer.Constant(0.0),regularizer=L2Decay(0.))
    )
    out=fluid.layers.leaky_relu(conv0_norm, alpha=0.1)
    return out

# 骨干网络
def Darknet53(inputImg,use_cudnn=True):
    # 预处理的两层conv
    conv0_norm=SmallConvBlock(inputImg,num_filter=32,filter_size=3)
    conv1_norm=SmallConvBlock(conv0_norm,num_filter=64,filter_size=3,stride=2)

    ## 第一个残差块
    conv0_R0_norm=SmallConvBlock(conv1_norm,num_filter=32,filter_size=1)
    conv1_R0_norm=SmallConvBlock(conv0_R0_norm,num_filter=64,filter_size=3)
    out_R0 = fluid.layers.elementwise_add(conv1_R0_norm, conv1_norm)
    R0_norm=SmallConvBlock(out_R0,num_filter=128,filter_size=3,stride=2)

    ## 第2个残差块

    conv0_R1 = []
    conv0_R1_norm = []
    conv1_R1 = []
    conv1_R1_norm = []
    out_R1 = []

    for i in range(2):
        if i == 0:
            inLayer = R0_norm
        else:
            inLayer = out_R1[i - 1]
        conv0_R1_norm.append(SmallConvBlock(inLayer,num_filter=64,filter_size=1,stride=1))
        conv1_R1_norm.append(SmallConvBlock(conv0_R1_norm[i],num_filter=128,filter_size=3,stride=1))
        out_R1.append(fluid.layers.elementwise_add(inLayer, conv1_R1_norm[i]))
    R1_norm =SmallConvBlock(out_R1[-1],num_filter=256,filter_size=3,stride=2)


    ## 第3个残差块

    conv0_R2 = []
    conv0_R2_norm = []
    conv1_R2 = []
    conv1_R2_norm = []
    out_R2 = []

    for i in range(8):
        if i == 0:
            inLayer = R1_norm
        else:
            inLayer = out_R2[i - 1]
        conv0_R2_norm.append(SmallConvBlock(inLayer,num_filter=128,filter_size=1,stride=1))
        conv1_R2_norm.append(SmallConvBlock(conv0_R2_norm[i],num_filter=256,filter_size=3,stride=1))
        out_R2.append(fluid.layers.elementwise_add(inLayer, conv1_R2_norm[i]))

    C2 = out_R2[-1]
    R2_norm=SmallConvBlock(C2,num_filter=512,filter_size=3,stride=2)

    # 第四个残差块

    conv0_R3 = []
    conv0_R3_norm = []
    conv1_R3 = []
    conv1_R3_norm = []
    out_R3 = []

    for i in range(8):
        if i == 0:
            inLayer = R2_norm
        else:
            inLayer = out_R3[i - 1]
        conv0_R3_norm.append(SmallConvBlock(inLayer,num_filter=256,filter_size=1,stride=1))
        conv1_R3_norm.append(SmallConvBlock(conv0_R3_norm[i],num_filter=512,filter_size=3,stride=1))
        out_R3.append(fluid.layers.elementwise_add(inLayer, conv1_R3_norm[i]))
    C1 = out_R3[-1]
    R3_norm = SmallConvBlock(C1,num_filter=1024,filter_size=3,stride=2)

    # 第五个残差块

    conv0_R4 = []
    conv0_R4_norm = []
    conv1_R4 = []
    conv1_R4_norm = []
    out_R4 = []

    for i in range(4):
        if i == 0:
            inLayer = R3_norm
        else:
            inLayer = out_R4[i - 1]
        conv0_R4_norm.append(SmallConvBlock(inLayer,num_filter=512,filter_size=1,stride=1))
        conv1_R4_norm.append(SmallConvBlock(conv0_R4_norm[i],num_filter=1024,filter_size=3,stride=1))
        out_R4.append(fluid.layers.elementwise_add(inLayer, conv1_R4_norm[i]))
    C0 = out_R4[-1]
    return C0, C1, C2


# yolo网络
def yoloMain(C0, outDim):
    conv0_C0_norm =SmallConvBlock(C0,num_filter=512,filter_size=1)
    conv1_C0_norm =SmallConvBlock(conv0_C0_norm,num_filter=1024,filter_size=3)
    conv2_C0_norm =SmallConvBlock(conv1_C0_norm,num_filter=512,filter_size=1)
    conv3_C0_norm =SmallConvBlock(conv2_C0_norm,num_filter=1024,filter_size=3)
    route =SmallConvBlock(conv3_C0_norm,num_filter=512,filter_size=1)
    tip =SmallConvBlock(route,num_filter=1024,filter_size=3)
    P0 = SmallConvBlock(tip,num_filter=outDim,filter_size=1)
    
    return route, tip, P0


def yolo3LossNet(P0_notReshape, inputLabel, anchorNum=3):
    shape=P0_notReshape.shape
    eachDim=shape[-3]//anchorNum
    rowNum=shape[-2]
    colNum=shape[-1]
    P0_reshape = fluid.layers.reshape(
        x=P0_notReshape,
        shape=[-1, anchorNum, eachDim, shape[-2], shape[-1]]
    )

    pred_Obj = P0_reshape[:, :, 4, :, :]  # 有没有物体1个
    # print(pred_Obj)

    tx = P0_reshape[:, :, 0, :, :]  # 位置四个
    ty = P0_reshape[:, :, 1, :, :]
    tw = P0_reshape[:, :, 2, :, :]
    th = P0_reshape[:, :, 3, :, :]

    pred_class = P0_reshape[:, :, 5:eachDim, :, :]  # 类别C个

    # inputLabel = fluid.layers.data("label", [None, anchorNum, eachDim, rowNum, colNum], dtype="float32")
    # 物体损失
    lossObj = fluid.layers.sigmoid_cross_entropy_with_logits(pred_Obj, inputLabel[:, :, 4, :, :],
                                                             ignore_index=-1)  # 物体损失
    # 位置损失
    lossX = fluid.layers.sigmoid_cross_entropy_with_logits(tx, inputLabel[:, :, 0, :, :])  # 位置损失
    lossY = fluid.layers.sigmoid_cross_entropy_with_logits(ty, inputLabel[:, :, 1, :, :])
    lossW = fluid.layers.abs(tw - inputLabel[:, :, 2, :, :])
    lossH = fluid.layers.abs(th - inputLabel[:, :, 3, :, :])
    # 类别损失
    lossClass = fluid.layers.sigmoid_cross_entropy_with_logits(pred_class, inputLabel[:, :, 5:eachDim, :, :])
    lossClass = fluid.layers.reduce_sum(lossClass, dim=2, keep_dim=False)

    # 排除未标签的非1物体
    unCount = inputLabel[:, :, 4, :, :] > 0
    unCount = fluid.layers.cast(unCount, dtype="float32")
    unCount.stop_gradient = True

    # 计算全部损失
    # print(lossObj, lossY, lossClass, unCount)
    lossPosition = (lossX + lossY + lossW + lossH) * unCount
    lossClass = lossClass * unCount
    lossAll = lossObj + lossPosition*1.5 + lossClass*10
    lossAll = fluid.layers.reduce_sum(lossAll, dim=[1, 2, 3], keep_dim=False)
    lossAve = fluid.layers.mean(lossAll)
    return lossAve
