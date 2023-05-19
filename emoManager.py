# determine when the negative emotion is detected
# determine when and what to display

from collections import Counter
import matplotlib.pyplot as plt
import utility
from playsound import playsound
from matplotlib.widgets import Button

# N continious negative same emotion in one list
def checkOneList_neg(labels):
    flag1=False
    continousTime=2
    if len(labels) != 0:  # if the list content elements
        flag1 = (len(labels[-1*continousTime:]) == continousTime) & \
                (len(set(labels[-1*continousTime:])) == 1) & \
                (labels[-1] in [1, 2, 3, 4])

    return flag1

# check 2 lists and decide to vibrate
def decideNeg(list1,list2):
    flag= checkOneList_neg(list1) | checkOneList_neg(list2) # if any of them contain continious negative same emotion
    return flag

# decide if the emotions imbalance
def checkOneList_b(labels,totalRun):
    flag = False  # not imbalanced

    if len(labels) != 0:  # if the list content elements
        total=len(labels) #total number of emotion labels
        mostCom=Counter(labels).most_common(1) # count the numbers of each emotion and find the most
        # the post has been browsed for a while
        # the most common emotion take up more than half of all emotions
        # fulfill the 2 conditions at the same time->imbalance
        flag= (total>=totalRun) & (mostCom[0][1]/total>=0.50)

    return flag


# check 2 lists and decide to display
def decideBalance(list1,list2,totalRun):
    flag= checkOneList_b(list1,totalRun) | checkOneList_b(list2,totalRun) # if any of them contain continious negative same emotion
    return flag

# convert label list to pie chart input data
# input: list
# output: two lists, the number of emotions and their emotion names
def convertLabel(labels):
    num_label=len(labels)

    #dictionary for translate the digit labels to emotion names
    emoDict0=utility.getEmoCode('')
    emoDict=dict(zip(emoDict0.values(), emoDict0.keys())) # reverse key and value

    # count the number of emotion labels for each emotion
    counted = Counter(labels)
    # translate the digit labels to emotion names
    for k in list(counted):
        counted[emoDict[k]] = counted.pop(k)
    oldValues=list(counted.values())
    newValues= [x/num_label for x in oldValues]

    # set colors in the pie chart consistent
    colorDict=utility.getEmoCode('color')
    colorList=counted.keys()
    colorList=[colorDict[x] for x in colorList]

    return newValues,list(counted.keys()),colorList


# display emotions
# pie chart
def displayEmo(list_text, list_face):
    fig, axes = plt.subplots(1, 2)
    # text analysis display
    if(len(list_text)>0):
        values,labels,colorList=convertLabel(list_text)
        axes[0].pie(values,labels=labels,colors=colorList)
        axes[0].set_title('emotions analysed via text')

    # face analysis display
    if(len(list_face)>0):
        values, labels,colorList = convertLabel(list_face)
        axes[1].pie(values,labels=labels,colors=colorList)
        axes[1].set_title('emotions analysed via images')

    #button to play the meditation
    buttonPos = fig.add_axes([0.94, 0.03, 0.06, 0.03])
    button= Button(buttonPos, 'play', color='khaki', hovercolor='yellow')
    callback=myButtonCbk()
    # pass parameters
    callback.list_face=list_face
    callback.list_text = list_text

    return button,callback, fig
    # # listen and callback
    # button.on_clicked(callback.playMeditation)
    # fig.show()

class myButtonCbk():
    list_text=[]
    list_face=[]
    # play the meditation according to the most common emotion
    # combine the lists from text and face
    def playMeditation(self,event):
            # count most common emotion
            allList=self.list_face+self.list_text
            mostCommon = Counter(allList).most_common(1)[0][0]
            fileName='audio/'+utility.getEmoCode('sound')[mostCommon]
            print('playing: '+fileName)
            # play the sound
            playsound(fileName)

