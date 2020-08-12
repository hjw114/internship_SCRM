'''
此模块的功能为比对人脸测试
author：胡觉文
'''
import pickle
import cv2
import numpy as np

class Predictor(object):#模型训练器
    def __init__(self,model_file):
        with open(model_file,'rb') as infile:
            self.loaded = pickle.load(infile)
        self.model = self.loaded['model']
        self.pca = self.loaded['pca_fit']
        self.label_encoder = self.loaded['label_encoder']
    def cv_imread(self,file_path):
        cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
        return cv_img

    def predict(self,img_file):#实现分类逻辑
        '''读取图像文件'''
        img = self.cv_imread(img_file)
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img_gray,(256,256))
        h,w = img.shape
        img_col = np.array([img.reshape(h*w)])
		#对图片进行transform 得到特征
        X_test_pca =self.pca.transform(img_col)
        y = self.model.predict(X_test_pca)
        print(y)
        return y
predictor = Predictor('./model/model_svm_poly_test010412.pkl')
label = predictor.predict(r"D:\openvino\workspaces\start-history\SVM-PCA_face_try\test\2_1.jpg")