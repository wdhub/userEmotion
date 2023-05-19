# analyse the result from FaceReader datasheet
# percentage of emotions in prototype test, except neutral/unknown

import utility
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import cv2

# read datasheet
df = pd.read_excel(r'FR.xls')
data=df.loc[:,['Dominant Expression','Analysis Index']].values

# select prototype data & separate users

def selectData(data, index):
    # select participant
    data1 = data[data[:, 1] == index]

    # clear other emotions
    data_P1 = data1[data1[:, 0] != 'Unknown']
    data_P1 = data_P1[data_P1[:, 0] != 'Neutral']
    data_P1 = data_P1[data_P1[:, 0] != 'END']

    # keep emotion labels
    data_P1 = data_P1[:, 0]

    return data_P1


dataList=[]
dataList.append(selectData(data,'Analysis 7')) # p1
dataList.append(selectData(data,'Analysis 10'))# p2
dataList.append(selectData(data,'Analysis 11'))# p3
dataList.append(selectData(data,'Analysis 14'))# p4


# display & save
def showResult(index,labels):
    fig = plt.figure()
    num_label=len(labels)
    counted = Counter(labels)
    oldValues = list(counted.values())
    newValues = [x / num_label for x in oldValues]

    colorDict = utility.getEmoCode('color_F')
    colorList = counted.keys()
    colorList = [colorDict[x] for x in colorList]

    plt.pie(newValues, labels=list(counted.keys()), colors=colorList)
    plt.title('emotions analysed via FaceReader')

    # plt.show()
    plt.savefig("FR_"+str(index)+".png")

index=0
for labels in dataList:
    showResult(index, labels)
    index+=1

# compare python result and FR result
indexs=range(0,4)
for ii in indexs:
    img1 = cv2.imread('pythonEmo/Figure_'+str(ii+1)+'.png')
    img2=cv2.imread('pythonEmo/FR_'+str(ii)+'.png')
    img = cv2.hconcat([img1, img2])
    cv2.imwrite('pythonEmo/Fig_' + str(ii+1) + '.png',img)

