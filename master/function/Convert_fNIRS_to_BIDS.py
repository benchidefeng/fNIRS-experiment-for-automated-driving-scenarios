import numpy as np
# from scipy import io
import os
import mne
import glob
import pdb
import nibabel as nib
import scipy.io as scio
import os.path as op
import shutil

from mne_bids import write_raw_bids, BIDSPath, print_dir_tree
from mne_bids.stats import count_events
from bids_validator import BIDSValidator
# from mne.io import concatenate_raws
# from mne.bids import BIDSPath, write_raw_bids
#import sys
#print(sys.executable)
fnirs_data="D:/zhangxiaofei/Scientific_Data/Figshare/NewDataset/02_Raw_to_SNIRS"
bids_root="D:/zhangxiaofei/Scientific_Data/Figshare/NewDataset/03_bids"

if op.exists(bids_root):
    shutil.rmtree(bids_root)

def fun_invalid_data(sub_i,current_task):

    with open('InvalidData.txt', 'r') as file:# 逐行读取文档内容
        data_array = []# 创建一个空数组
        for line in file:
            pairs = line.strip().split()   # 按空格分割每行中的数
            temp_array = [] # 创建一个临时数来存储每行的数
            for pair in pairs:
                key, value = pair.split(':')
                temp_array=np.append(temp_array,value) # 将临时数添加到最终数组中
            data_array=np.append(data_array,temp_array)
            data_array2d=data_array.reshape(-1, 2)
        # print(data_array2d)# 打印保存的数组内容 
    data_found=False
    for row in range(data_array2d.shape[0]):
        # pdb.set_trace()
        if int(data_array2d[row,0])==sub_i and int(data_array2d[row,1])==int(current_task):
            data_found = True
            break

    return data_found
def fun_get_sti(file_path,sti_data):
    file_name,format_name=file_path.split('.')
    current_seg=file_name[-3:]  
    current_task=(int(file_name[-3])-1)*2+(int(file_name[-1]))
    # current_task="Task"+str(current_task_num)
    current_task_str=str(current_task)
    sti_array = np.array([])
    for num_i in range(0, int(sti_data.size/3)):
        if sti_data[num_i][0][0]==current_seg:
            sti_array=np.append(sti_array,[sti_data[num_i][2][0][0],0,sti_data[num_i][1][0][0]])
        else:
            aa=1
    
    sti_array = sti_array.reshape(-1, 3)   
    return sti_array,current_task_str
##############################################################################################################

for sub_i in range(1, 21):
    fnirs_data_sub=fnirs_data+"/sub_"+str(sub_i)
    print("fnirs_data_sub位置：", fnirs_data_sub)
    fnirs_files = glob.glob(os.path.join(fnirs_data_sub, "*.snirf"))
    sti_files = glob.glob(os.path.join(fnirs_data_sub, "*.mat"))
    sti_data_dict = scio.loadmat(sti_files[0])
    for file_path in fnirs_files:
        print(file_path)
        raw_od= mne.io.read_raw(file_path, preload=False)  
        raw_od.info["line_freq"] = 50  # specify power line frequency as required by BIDS
        sti_data=sti_data_dict['snirf_stim']
        sti_array02,current_task=fun_get_sti(file_path,sti_data)
        # description = [str(x) for x in sti_array02[:, 2]]
        Flag_valid02=fun_invalid_data(sub_i,current_task)
        if Flag_valid02:
            print("数据为无效数据不进行转换：")
        else:
            annotations01 = mne.Annotations(onset=sti_array02[:, 0]/50,  # 刺激发生的时间点
                                        duration=sti_array02[:, 1],  # 持续时间为 0 表示这些事件点只是事件的发生点
                                        description = [str(x) for x in sti_array02[:, 2]])
            raw_od.set_annotations(annotations01)
            events, event_id = mne.events_from_annotations(raw_od)
            
            bids_path = BIDSPath(subject=str(sub_i), task=current_task, root=bids_root)
            # pdb.set_trace()
            write_raw_bids(raw_od, bids_path, overwrite=True)
     