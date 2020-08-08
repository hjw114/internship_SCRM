import os
import cv2
import numpy as np
from PIL import Image

#注意图片的命名格式为User.id.sampleNum
def get_images_and_labels(path,detector):#创建一个函数，用于从数据集文件夹中获取训练图片,并获取id
    image_paths = [os.path.join(path,f) for f in os.listdir(path)]
    face_samples = []
    ids = []
    for image_path in image_paths:#遍历图片路径，导入图片和id添加到list中
        img = Image.open(image_path).convert('L')#通过图片路径将其转换为灰度图片
        img_np = np.array(img,'uint8')#将图片转化为数组
        if os.path.split(image_path)[-1].split(".")[-1] != 'jpg':
            continue
        id = int(os.path.split(image_path)[-1].split(".")[0])#为了获取id，将图片和路径分裂并获取
        faces = detector.detectMultiScale(img_np)
        for(x,y,w,h) in faces:#将获取的图片和id添加到list中
            face_samples.append(img_np[y:y+h,x:x+w])
            ids.append(id)
    return face_samples,ids

def train(path,detector):
    recog = cv2.face.LBPHFaceRecognizer_create()  # 初始化识别的方法
    print('Training...')
    faces, ids = get_images_and_labels(path,detector)  # 训练模型
    recog.train(faces, np.array(ids))  # 保存模型
    recog.save(r'D:\internship_SCRM\face\model\trainer.yml')

if __name__ == '__main__':
    path = 'D:/internship_SCRM/face/face'
    detector = cv2.CascadeClassifier(
        r'F:\Anaconda3\envs\openvino\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')  # 调用人脸分类器
    train(path,detector)