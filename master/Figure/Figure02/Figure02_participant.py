import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import pdb
x=('sub1','sub2','sub3','sub4','sub5','sub6','sub7','sub8','sub9','sub10','sub11','sub12','sub13','sub14','sub15','sub16','sub17','sub18','sub19','sub20')
age=[24,46,42,41,25,21,32,22,28,24,25,25,25,32,31,24,41,33,24,26]
colors=['lightgray','lightblue','lightblue','lightgray','lightgray','lightgray','lightgray','lightgray','lightgray','lightgray','lightblue','lightgray','lightblue','lightblue','lightgray','lightgray','lightgray','lightgray','lightgray','lightgray']
driving=[0,0,3,17,7,0,0,0,0,0,0,0,0,0,0,0,10,3,1,5]
font1 = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 12,
        }
fig=plt.figure()
#fig(figsize=(10, 5))
ax1 = fig.add_subplot(111)
ax1.bar(x, age,color=colors)
for a, b in zip(x, age):
        plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=10)
plt.xlabel('number',font1)
plt.xticks(rotation=70) # 倾斜70度
plt.ylabel('age',font1)
green_patch = mpatches.Patch(color='lightgray', label='Male')

yellow_patch = mpatches.Patch(color='lightblue', label='Female')
pdb.set_trace()
plt.legend(handles=[green_patch, yellow_patch])
ax2 = ax1.twinx()
ax2.plot(x,driving,color='red')
plt.xlabel('number',font1)
plt.ylabel('driving experience',font1)
plt.gcf().set_size_inches(10, 5)
#plt.title('subject information')
pdf = PdfPages('Figure02_participant.pdf')
pdf.savefig()
plt.close()
pdf.close()
#plt.show()