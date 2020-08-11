import cv2

def judge(video_id):
    jud=0
    num=0
    con=0
    id=None
    recognizer = cv2.face.LBPHFaceRecognizer_create()#LBPH识别方法
    recognizer.read(r'D:\internship_SCRM\face\model\trainer.yml')#读入之前训练好的模型
    faceCascade = cv2.CascadeClassifier(
        r'F:\Anaconda3\envs\openvino\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')#调用人脸分类器
    cam = cv2.VideoCapture(r"D:\internship_SCRM\face\face_video\%s.mp3"%(video_id))#调用摄像头
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )#识别人脸
        for (x, y, w, h) in faces:#进行校验
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < 100:
                jud = jud + 1
                num = num + 1
                con_r = 100 - confidence
                if con_r >= 50:
                    jud = 1
                if (con_r >= con ):
                    con = con_r
                    id = idnum
            else:
                jud = jud - 1
                num=num+1
        cv2.imshow('image', img)  # 显示图片
        k = cv2.waitKey(1)
        if k == 27:
            break
        elif num == 100:
            break
    cam.release()
    cv2.destroyAllWindows()
    if jud == 1:#判断是否是新用户
        return id
    else:
        return -1

if __name__ == '__main__':
    judge(0)