# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 15:28:58 2017

@author: yangpuhai
"""
import os
from sklearn import svm
from sklearn.externals import joblib
from url_feature_extract import url_feature_extract as ufe

def load_data(filename):
    f=open(filename,'r')
    data=f.readlines()
    x=[]
    y=[]
    for d in data:
        x.append(ufe(d))
        y.append(1)
    return x,y

def create_model():
    train_x,train_y=load_data('training_data\webpage_url_2')
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    clf.fit(train_x)
    if os.path.exists('filter_model')==False:
        os.mkdir('filter model')
    joblib.dump(clf, "filter_model/train_model_2.m")
    return True

def load_model():
    clf = joblib.load("filter_model/train_model_2.m")
    return clf

def model_prediction(model,url):
    return model.predict(ufe(url))
    
if __name__ == '__main__':
    create_model()



'''
if __name__ == '__main__':
    
    x,y=load_data('training_data\webpage_url_2')
    f=open('training_data_vector.txt','a')
    for x1 in x:
        f.write(str(x1))
        f.write('\n')
    f.close()
    
    create_model()
    print 'model create success'
    
    test_x=[]
    test_y=[]
    clf = joblib.load("train_model_2.m")
    f=open('training_data\webpage_url_2_test12','r')
    data=f.readlines()
    for d in data:
        s=d.split(' ')
        test_x.append(ufe(s[0]))
        test_y.append(float(s[1]))
    result=clf.predict(test_x)
    print result
    TP=0
    FP=0
    FN=0
    TN=0
    for i in range(0,len(result)):
        if result[i]==1 and test_y[i]==1:
            TP+=1
        if result[i]==1 and test_y[i]==-1:
            FP+=1
        if result[i]==-1 and test_y[i]==1:
            FN+=1
        if result[i]==-1 and test_y[i]==-1:
            TN+=1
    count=len(result)
    print '测试数据：',count
    print 'TP:',TP
    print 'FP:',FP
    print 'FN:',FN
    print 'TN:',TN
    P=TP*1.0/(TP+FP)
    R=TP*1.0/(TP+FN)
    print '精确率：',P
    print '召回率：',R
    print 'F1：',2*P*R/(P+R)
'''



