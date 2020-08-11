'''
本模块的功能为集成人脸识别功能
author：胡觉文
'''
import cv2
import os
import get
import LBPHFaceRecognizer
import judge_people
import sql_data

def master(video_id):#集成人脸识别
    if os.path.exists(r'D:\internship_SCRM\face\model\trainer.yml'):#判断是否训练过
        if judge_people.judge(video_id) == -1:
            ids = sql_data.serach()#查找数据
            sql_data.add(ids[-1] + 1)# 添加数据
            get.get(video_id,ids[-1] + 1)
            path = 'D:/internship_SCRM/face/face'
            detector = cv2.CascadeClassifier(
                r'F:\Anaconda3\envs\openvino\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')# 调用人脸分类器
            LBPHFaceRecognizer.train(path,detector)
            os.remove(r"D:\internship_SCRM\face\face_video\%s.mp3"%(video_id))#删除视频文件
            return -1
        else:
            os.remove(r"D:\internship_SCRM\face\face_video\%s.mp3" % (video_id))#删除视频文件
            return judge_people.judge(video_id)
    else:
        id = sql_data.serach()#查找数据
        sql_data.add(id[-1] + 1)# 添加数据
        get.get(video_id,id[-1] + 1)
        path = 'D:/internship_SCRM/face/face'
        detector = cv2.CascadeClassifier(
            r'F:\Anaconda3\envs\openvino\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')# 调用人脸分类器
        LBPHFaceRecognizer.train(path,detector)
        os.remove(r"D:\internship_SCRM\face\face_video\%s.mp3" % (video_id))#删除视频文件
        return -2

if __name__ == '__main__':
    master(0)