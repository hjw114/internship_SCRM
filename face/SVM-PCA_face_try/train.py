'''
此模块功能为SVM-PCA训练人脸
author：胡觉文
'''
import numpy as np
import os
import cv2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
from sklearn.metrics import classification_report
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from time import time
from sklearn.model_selection import GridSearchCV

def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)  # 打开文件中含有中文路径的图片
    return cv_img

def search_files(directory):
    images = []
    labels = []
    for curdir, subdir, files in os.walk(directory):  # 根据路径,得到文件夹的的地址, 下面的子目录名称, 目录下的所有文件
        for file in files:
            if file.endswith('.jpg'):
                label = curdir.split(os.path.sep)[-1]  # 用分隔符'\' 进行切割,得到所在的文件夹最后一个单词,作为标签
                path = os.path.join(curdir, file)  # 拼接路径
                img = cv_imread(path)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.resize(img_gray, (256, 256))
                h, w = img.shape
                img_col = img.reshape(h * w)
                images.append(img_col)
                labels.append(label)
    return images, labels

def save_model(model, pca, label_encoder, output_file):
    try:
        with open(output_file, 'wb') as outfile:
            pickle.dump({
                'model': model,
                'pca_fit': pca,
                'label_encoder': label_encoder
            }, outfile)
        return True
    except:
        return False

img, labels = search_files('./face')
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)
X, Y = np.array(img), np.array(labels)
train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.2, random_state=None)
t0 = time()
pca = PCA(n_components=20, svd_solver='randomized', whiten=True).fit(train_x)  # 取20个特征,并且fit 这个train_x
print("done in %0.3fs" % (time() - t0))
X_train_pca = pca.transform(train_x)  # 得到训练集投影系数
X_test_pca = pca.transform(test_x)  # 得到测试集投影系数
param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
              'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
clf = GridSearchCV(SVC(kernel='poly', class_weight='balanced'), param_grid)
clf = clf.fit(X_train_pca, train_y)
output_dir = './model'
print("Best estimator found by grid search:")
print(clf.best_estimator_)
y_pred = clf.predict(X_test_pca)
print("done in %0.3fs" % (time() - t0))
print(classification_report(test_y, y_pred))
save_model(clf, pca, label_encoder, os.path.join(output_dir, 'model_svm_poly_test010412.pkl'))