# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 16:47:48 2022

@author: 86188
"""
###############################load python module##########################
import numpy as np
import os
import pdb
import scipy.io as scio
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import pandas as pd

Nub_Sub=20
Nub_Index=3
# All_Scenario=['Scenario1.mat','Scenario2.mat','Scenario3.mat','Scenario4.mat',
#                 'Scenario5.mat','Scenario6.mat','Scenario7.mat','Scenario8.mat',
#                 'Scenario9.mat','Scenario10.mat','Scenario11.mat','Scenario12.mat',
#                 'Scenario13.mat','Scenario14.mat']
All_Scenario=['Scenario1','Scenario2','Scenario3','Scenario4',
                'Scenario5','Scenario6','Scenario7','Scenario8',
                'Scenario9','Scenario10','Scenario11','Scenario12',
                'Scenario13','Scenario14']
#########################obtain data position######################
def get_risk_index(Risk_All):
    Scenario_Nub=0
    Scenario_Point=Risk_All[0].shape[1]
    # print(Scenario_Point)
    Scenario_Index=np.zeros([Nub_Index,Scenario_Point])
    Scenario_Data=[]
    for i_sub in range(Nub_Sub):
        for i_scen in range(Risk_All[i_sub].shape[0]):
            Scenario_Data.append(Risk_All[i_sub][i_scen,:])
#################################################################################
    Scenario_Data_array=np.zeros([len(Scenario_Data),Scenario_Point])
    for i_data in range(len(Scenario_Data)):
        Scenario_Data_array[i_data,:]=Scenario_Data[i_data]
    for i_point in range(Scenario_Point):
        Scenario_Index[0,i_point]=np.max(Scenario_Data_array[:,i_point])
        Scenario_Index[1,i_point]=np.mean(Scenario_Data_array[:,i_point])
        Scenario_Index[2,i_point]=np.min(Scenario_Data_array[:,i_point])
    return Scenario_Index

#########################obtain data position######################
def fun_plot_figure(Risk_All):
    fig = plt.figure()
    # gs = gridspec.GridSpec(3, 3, width_ratios=[1, 1], height_ratios=[1, 1])
    gs = gridspec.GridSpec(5, 3)
    plt.rcParams['font.size'] = 5
    # pdb.set_trace()
    for key,value in Risk_All.items():
         key_list = key.split(".")
         Scenario_name=key_list[0]

         i_nub_scenarin=All_Scenario.index(key)
         [axs_0,axs_1]=divmod(i_nub_scenarin, 3)
         ax1 = fig.add_subplot(gs[axs_0, axs_1])
         X=range(value.shape[1])
         X= [nub_i * 0.01 for nub_i in X]
         max_value =value[0,:]
         mean_value=value[1,:]
         min_value =value[2,:]
         ax1.plot(X,max_value,c='skyblue')
         ax1.plot(X,mean_value,c='red')
         ax1.plot(X,min_value,c='skyblue')
         ax1.fill_between(X,mean_value, max_value,facecolor='skyblue',interpolate=True,alpha=1)#区域填
         ax1.fill_between(X,min_value, mean_value,facecolor='skyblue',interpolate=True,alpha=1)#区域填
         ax1.xaxis.set_major_locator(ticker.MultipleLocator(5))
         ax1.set_title(Scenario_name, fontsize=6)
         ax1.set_xlim(0,40)
        #  ax1.set_title('Title', fontsize=12)
        #  ax1.set_xlabel('Time', fontsize=6)
        #  ax1.set_ylabel('Risk', fontsize=6)
         ax1.tick_params(axis='both', labelsize=6)
         i_nub_scenarin=i_nub_scenarin+1
    gs.update(wspace=0.3, hspace=1)
    
    plt.savefig('Figure_Risk.pdf', format='pdf')
    plt.show()
    
    #     #  plt.show()
    #      del axs, fig, value
    # plt.savefig('figure.pdf', format='pdf')

#########################obtain data position######################
Current_Data=os.getcwd()
print(Current_Data)
parent_directory = os.path.dirname(Current_Data)
grandparent_directory = os.path.dirname(parent_directory)
Position_Event_Data=grandparent_directory+'\example\data\VehicleStatusDataset'
print ('The position of data is', Position_Event_Data)
Name_Event=os.listdir(Position_Event_Data)
Scenario_Indexall={}
for i_event in Name_Event:#####load each event data
    # print ('################################################')
    # print ('It is dealing with the Scenario of', i_event)
    Scenario_Data_Position=Position_Event_Data+'\\'+i_event
    # Scenario_Data=scio.loadmat(Scenario_Data_Position)
    # Scenario_Data = pd.read_csv(Scenario_Data_Position)

    Risk_All = []

    # 遍历路径下的文件夹
    for folder in os.listdir(Scenario_Data_Position):
        if folder.startswith('Sub') and folder[3:].isdigit():
            folder_path = os.path.join(Scenario_Data_Position, folder)
            csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
            folder_data = []
            for file in csv_files:
                file_path = os.path.join(folder_path, file)
                df = pd.read_csv(file_path)
                column_13 = df.iloc[:, 12]
                folder_data.append(column_13)
            Risk_All.append(np.array(folder_data))

    Scenario_Index01=get_risk_index(Risk_All)
    Scenario_Indexall.update({i_event:Scenario_Index01})
fun_plot_figure(Scenario_Indexall)
# pdb.set_trace() 
    # Event_Data_Position=Position_Data+str(i_event+1)
    # Name_Event_People=os.listdir(Event_Data_Position)
    # Dataset={}
    # for i_event_people in Name_Event_People:#####load each people data   
    #     People_Position_Data=Event_Data_Position+'\\'+i_event_people
    #     Name_subject='Sub'+str(i_event+1)
    #     # print ('################################################')
    #     # print ('It is dealing with the data of', People_Position_Data)
    #     People_Data=scio.loadmat(People_Position_Data)
    #     Effective_data=People_Data['Effective_Data']
    #     Scene_num=People_Data['Scene_num']
    #     Scene_Num_Int=Scene_num.astype(int)[0][0]-1
    #     # pdb.set_trace()
    #     Fragment_Effective_data=Effective_data[0:Scene_Num_Int,:,:]
    #     DatasetOnesub=SA.get_people_data(Fragment_Effective_data,i_event_people)
    #     Dataset.update(DatasetOnesub)
    #     # pdb.set_trace()
    
    # Event_Data_Name=Current_Data+'\Dataset\\'+'Scenario'+str(i_event+1)+'.mat'
    # # pdb.set_trace()
    # scio.savemat(Event_Data_Name,Dataset)
    # del i_event_people, Name_Event_People, Dataset
    # # pdb.set_trace()
