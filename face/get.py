import cv2
import sql_data

def get(face_id):
    cap = cv2.VideoCapture(0)  # 调用笔记本内置摄像头，参数为0，如果有其他的摄像头可以调整参数为1,2
    face_detector = cv2.CascadeClassifier(
        r'F:\Anaconda3\envs\openvino\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')  # 调用人脸分类器
    count = 0  # sampleNum用来计数样本数目
    while True:
        success, img = cap.read()  # 从摄像头读取图片
        if success is True:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转为灰度图片，减少程序符合，提高识别度
        else:
            break
        faces = face_detector.detectMultiScale(gray, 1.3,
                                               5)  # 检测人脸，将每一帧摄像头记录的数据带入OpenCv中，让Classifier判断人脸,其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为minNeighbors
        for (x, y, w, h) in faces:  # 框选人脸，for循环保证一个能检测的实时动态视频流
            cv2.rectangle(img, (x, y), (x + w, y + w), (255, 0, 0))  # xy为左上角的坐标,w为宽，h为高，用rectangle为人脸标记画框
            count += 1  # 成功框选则样本数增加
            cv2.imwrite(
                "D:/internship_SCRM/face/face/" + str(face_id) + '.' + str(count) + '.jpg',
                gray[y:y + h, x:x + w])  # 保存图像，把灰度图片看成二维数组来检测人脸区域
            cv2.imshow('image', img)  # 显示图片
        k = cv2.waitKey(1)  # 保持画面的连续。waitkey方法可以绑定按键保证画面的收放，通过q键退出摄像
        if k == '27':
            break
        elif count >= 800:
            break
    cap.release()  # 关闭摄像头，释放资源
    cv2.destroyAllWindows()
    return face_id

if __name__ == '__main__':
    #id = sql_data.serach()
    #sql_data.add(id[-1] + 1)
    get(0)