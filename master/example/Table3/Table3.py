# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 19:49:46 2023

@author: 86188
"""

import numpy as np
import pandas as pd
from scipy import stats
import os
# import tensorflow as tf
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
###############################load python module##########################
import math
from sklearn import linear_model
# coding:UTF-8
import scipy.io as scio
import os.path
from sklearn.model_selection import train_test_split
import os
from sklearn.preprocessing import StandardScaler
import time
from sklearn.preprocessing import MinMaxScaler
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    recall_score,
    precision_score,
    accuracy_score
)

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn import naive_bayes,neighbors,discriminant_analysis
from sklearn.linear_model import LogisticRegression
import os.path
import os
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
# from keras import Sequential
# from keras.layers import LSTM,Activation,Dense,Dropout,Input,Embedding,BatchNormalization,Add,concatenate,Flatten
from sklearn.ensemble import AdaBoostClassifier
from sklearn.datasets import make_classification
import SDfNIRS
from xgboost import XGBClassifier
# from cut_fNIRS_data import fNIRS_cut
# from t_test_value import t_test
# from fNIRS_data_t_test import fNIRS_t_test
import pdb 
#EmergentAEB：Scenario 07
#left_cut_in：
def main():
    All_Event_Type = [ 'EmergentAEB','left_cut_in', 'right_cut_in','pedestrian_right']
    Num_Event = len(All_Event_Type)
    Result_Text='result.txt'
    if os.path.exists(Result_Text)==True:
        os.remove(Result_Text)
    else:
        aa=1
        
    random_seed = 42
    np.random.seed(random_seed)     
    ######Adaboosting######
    ada_clf = AdaBoostClassifier(
        # SVC(kernel='linear'), n_estimators=200,
        DecisionTreeClassifier(max_depth=13), n_estimators=200,
        # algorithm='SAMME', learning_rate=0.5
        algorithm='SAMME.R', learning_rate=0.5
    )
    
    

    rfClf = RandomForestClassifier(n_estimators=200, random_state=0)

    dtClf = DecisionTreeClassifier(max_depth=6, random_state=0,min_samples_leaf=10,min_samples_split=10)
    svmClf = SVC(probability=True, random_state=0)
    logClf = LogisticRegression(random_state=0) 
    XGBclf=XGBClassifier(booster= ['gbtree', 'dart', 'gblinear'])
    clf2 = VotingClassifier(estimators=[('rf', rfClf), ('svm', svmClf), ('dt', dtClf), ('log', logClf)], voting='soft')

    for i_event in All_Event_Type:  #####load each event data 
        DataSetOneevnt=SDfNIRS.obtain_data_from_dataset_cvs(i_event)
        Data_XX=DataSetOneevnt['Data_X']
        Data_Y=DataSetOneevnt['Data_Y']
        # pdb.set_trace()
        Data_XX = Data_XX.reshape(Data_XX.shape[0], 3200)
        # Data_X=np.mean(Data_XX,axis=1)
        # xa = xa.reshape(a, 3200)
        # pdb.set_trace()
        random_seed = 42
        X_train, X_test, Y_train, Y_test = train_test_split(Data_XX, Data_Y, test_size=0.2,random_state=random_seed)
    
        # pdb.set_trace()
        ######The training of AdaBoostClassifier######
        ada_clf.fit(X_train, Y_train)
        ada_clf_Training_Accuracy=ada_clf.score(X_train, Y_train)
        print('Accuracy AdaBoostClassifier train score', ada_clf_Training_Accuracy)
         ######The testing of AdaBoostClassifier######
        y_pred = ada_clf.predict(X_test)
        ada_clf_Testing_Accuracy=accuracy_score(Y_test, y_pred)
        print('Accuracy AdaBoostClassifier test score', ada_clf_Testing_Accuracy)
        SDfNIRS.save_reslut_to_text(Result_Text,i_event,Algorithm_Name='AdaBoost',Training_Accuracy=ada_clf_Training_Accuracy,Testing_Accuracy=ada_clf_Testing_Accuracy)

        ######The training of VotingClassifier######
        clf2.fit(X_train, Y_train)
        dclf2_Training_Accuracy=clf2.score(X_train, Y_train)
        print('Accuracy VotingClassifie train score', dclf2_Training_Accuracy)
        ######The testing of DecisionTree######
        Y_pred= clf2.predict(X_test)
        clf2_Testing_Accuracy = accuracy_score(Y_test, Y_pred)
        print('Accuracy VotingClassifie test score', clf2_Testing_Accuracy)
        SDfNIRS.save_reslut_to_text(Result_Text,i_event,Algorithm_Name='VotingClassifier',Training_Accuracy=dclf2_Training_Accuracy,Testing_Accuracy=clf2_Testing_Accuracy)
        del dclf2_Training_Accuracy, clf2_Testing_Accuracy,Y_pred

        ######The training of RandomForestClassifier######
        rfClf.fit(X_train, Y_train)
        rfClf_Training_Accuracy=rfClf.score(X_train, Y_train)
        print('Accuracy RandomForest train score', rfClf_Training_Accuracy)
        ######The testing of DecisionTree######
        Y_pred= rfClf.predict(X_test)
        rfClf_Testing_Accuracy = accuracy_score(Y_test, Y_pred)
        print('Accuracy RandomForest test score', rfClf_Testing_Accuracy)
        SDfNIRS.save_reslut_to_text(Result_Text,i_event,Algorithm_Name='RandomForest',Training_Accuracy=rfClf_Training_Accuracy,Testing_Accuracy=rfClf_Testing_Accuracy)
        del rfClf_Training_Accuracy, rfClf_Testing_Accuracy,Y_pred


if __name__ == '__main__':
    main()