'''
此模块的功能为获取人脸,初步处理
author：胡觉文
'''
import cv2
import os
from PIL import Image
import numpy as np

def get(id):
	vidcap = cv2.VideoCapture(0)
	count = 0
	success = True
	while success:
		success, image = vidcap.read()
		cv2.imwrite('D:/openvino/workspaces/start-history/CNN-lenet/face/%d_%d.jpg' % (id, count), image)
		if cv2.waitKey(10) == 27:
			break
		count += 1
		if count == 100:
			break

def read_data(data_dir):#读取人脸照片
    datas = []
    labels = []
    fpaths = []
    for fname in  os.listdir(data_dir):
        fpath = os.path.join(data_dir, fname)
        fpaths.append(fpath)
        image = Image.open(fpath)
        image = image.resize((150, 150), Image.ANTIALIAS)
        gray = image.convert('L')
        image_gray = np.expand_dims(gray, axis=2)
        image_gray = np.concatenate((image_gray, image_gray, image_gray), axis=-1)# 3通道灰度图
        data = np.array(image_gray) / 255.0
        label = int(fname.split("_")[0])
        datas.append(data)
        labels.append(label)
    datas = np.array(datas)
    labels = np.array(labels)
    print("shape of datas: {}\tshape of labels: {}".format(datas.shape, labels.shape))
    return fpaths, datas, labels

if __name__ == '__main__':
    #get(1)
    datas=read_data("D:/openvino/workspaces/start-history/CNN-lenet/face")
    print(datas)