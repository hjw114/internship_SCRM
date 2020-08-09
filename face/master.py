import cv2
import os
import get
import LBPHFaceRecognizer
import judge_people
import sql_data

def master():
    if os.path.exists(r'D:\internship_SCRM\face\model\trainer.yml'):#判断是否训练过
        if judge_people.judge() == -1:
            ids = sql_data.serach()#查找数据
            sql_data.add(ids[-1] + 1)  # 添加数据
            get.get(ids[-1] + 1)
            path = 'D:/internship_SCRM/face/face'
            detector = cv2.CascadeClassifier(
                r'F:\Anaconda3\envs\openvino\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')  # 调用人脸分类器
            LBPHFaceRecognizer.train(path,detector)
            return -1
        else:
            return judge_people.judge()
    else:
        id = sql_data.serach()
        sql_data.add(id[-1] + 1)
        get.get(id[-1] + 1)
        path = 'D:/internship_SCRM/face/face'
        detector = cv2.CascadeClassifier(
            r'F:\Anaconda3\envs\openvino\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
        LBPHFaceRecognizer.train(path,detector)
        return -2

if __name__ == '__main__':
    master()