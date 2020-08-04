import cv2
import os
import get
import LBPHFaceRecognizer
import judge_people
import sql_data

def master():
    if os.path.exists(r'D:\openvino\workspaces\start-history\face_try\model\trainer.yml'):#判断是否训练过
        names=sql_data.serach()#查找数据
        if judge_people.judge(names) == 0:
            get.get()
            path = 'D:/openvino/workspaces/start-history/face_try/face'
            detector = cv2.CascadeClassifier(
                r'F:\Anaconda3\envs\openvino\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')  # 调用人脸分类器
            LBPHFaceRecognizer.train(path,detector)
            ids=sql_data.serach()
            sql_data.add(ids[-1]+1)#添加数据
        else:
            return judge_people.judge(names)
    else:
        get.get()
        path = 'D:/openvino/workspaces/start-history/face_try/face'
        detector = cv2.CascadeClassifier(
            r'F:\Anaconda3\envs\openvino\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
        LBPHFaceRecognizer.train(path,detector)
        id = sql_data.serach()
        sql_data.add(id[-1] + 1)

if __name__ == '__main__':
    master()