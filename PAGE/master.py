import cv2
import os
import get
import LBPHFaceRecognizer
import judge_people
import sql_data

def master(path):
    if os.path.exists(r'E:\My Documents\GitHub\web\model\trainer.yml'):#判断是否训练过
        if judge_people.judge(path) == -1:
            ids = sql_data.serach()#查找数据
            sql_data.add(ids[-1] + 1)  # 添加数据
            get.get(ids[-1] + 1,path)
            path2 = 'E:/My Documents/GitHub/web/face'
            detector = cv2.CascadeClassifier(
                r'E:\USER\xue xi\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')  # 调用人脸分类器
            LBPHFaceRecognizer.train(path2,detector)
            return -1
        else:
            return judge_people.judge(path)
    else:
        id = sql_data.serach()
        sql_data.add(id[-1] + 1)
        get.get(id[-1] + 1,path)
        path2 = 'E:/My Documents/GitHub/web/face/'
        detector = cv2.CascadeClassifier(
            r'E:\USER\xue xi\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
        LBPHFaceRecognizer.train(path2,detector)
        return -2
"""
if __name__ == '__main__':
    print(master())
"""