'''
此模块的功能为设计lenet5网络，调参
author：胡觉文
'''
import get_face
import tensorflow as tf
tf.compat.v1.disable_eager_execution()

def lenet_face(train):#训练模型
    #fpaths, datas, labels = get_face.read_data("D:/openvino/workspaces/start-history/CNN-lenet/face")  # 获取人脸
    fpaths, datas, labels = get_face.read_data(r"D:\openvino\workspaces\start-history\CNN-lenet\test")  # 获取人脸
    num_classes = len(set(labels))  # 种类
    datas_placeholder = tf.compat.v1.placeholder(tf.float32, [None, 150, 150, 3])
    labels_placeholder = tf.compat.v1.placeholder(tf.int32, [None])  # 定义placeholder,存放数据和标签
    dropout_placeholder = tf.compat.v1.placeholder(tf.float32)  # 定义dropout参数容器
    conv0 = tf.compat.v1.layers.conv2d(datas_placeholder, 20, 5, activation=tf.nn.relu)  # 第一层卷积，20个卷积核，卷积核大小为5，激活函数relu
    pool0 = tf.compat.v1.layers.max_pooling2d(conv0, [2, 2], [2, 2])  # 第一层最大池化，窗口2*2，步长2*2
    conv1 = tf.compat.v1.layers.conv2d(pool0, 40, 4, activation=tf.nn.relu)  # 第二层卷积，40个卷积核，卷积核大小为4，激活函数relu
    pool1 = tf.compat.v1.layers.max_pooling2d(conv1, [2, 2], [2, 2])  # 第二层最大池化，窗口2*2，步长2*2
    flatten = tf.compat.v1.layers.flatten(pool1)  # 三维向量转换
    fc = tf.compat.v1.layers.dense(flatten, 400, activation=tf.nn.relu)  # 全连接层，转换特征向量
    dropout_fc = tf.compat.v1.layers.dropout(fc, dropout_placeholder)  # 防止过拟合
    logits = tf.compat.v1.layers.dense(dropout_fc, num_classes)  # 输出层
    predicted_labels = tf.compat.v1.arg_max(logits, 1)
    losses = tf.nn.softmax_cross_entropy_with_logits(labels=tf.one_hot(labels_placeholder, num_classes),
                                                     logits=logits)  # 损失函数为交叉熵
    mean_loss = tf.reduce_mean(losses)  # 平均损失
    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=1e-5).minimize(losses)  # Adam优化
    saver = tf.compat.v1.train.Saver()
    with tf.compat.v1.Session() as sess:
        if train:
            print("训练模式")
            sess.run(tf.compat.v1.global_variables_initializer())
            train_feed_dict = {
                datas_placeholder: datas,
                labels_placeholder: labels,
                dropout_placeholder: 0.5
            }
            for step in range(100):
                _, mean_loss_val = sess.run([optimizer, mean_loss], feed_dict=train_feed_dict)
                if step % 10 == 0:
                    print("step = {}\tmean loss = {}".format(step, mean_loss_val))
            saver.save(sess, "D:/openvino/workspaces/start-history/CNN-lenet/model/")
            print("训练结束， 保存模型到{}".format("D:\openvino\workspaces\start-history\CNN-lenet\model"))
        else:
            print("测试模式")
            saver.restore(sess, "D:/openvino/workspaces/start-history/CNN-lenet/model/")
            print("从{}导入模型".format("D:\openvino\workspaces\start-history\CNN-lenet\model"))
            test_feed_dict = {
                datas_placeholder: datas,
                labels_placeholder: labels,
                dropout_placeholder: 0
            }
            predicted_labels_val = sess.run(predicted_labels, feed_dict=test_feed_dict)
            for fpath, real_label, predicted_label in zip(fpaths, labels, predicted_labels_val):
                print("{}\t{} -> {}".format(fpath, real_label, predicted_label))

if __name__ == '__main__':
    #get_face.get(5)
    lenet_face(0)