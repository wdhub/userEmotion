# determine when the negative emotion is detected
# determine when and what to display

# three continious negative same emotion in one list
def checkOneList_neg(label2vibrate):
    flag1=False
    if len(label2vibrate) != 0:  # if the list content elements
        flag1 = (len(label2vibrate[-3:]) == 3) & \
                (len(set(label2vibrate[-3:])) == 1) & \
                (label2vibrate[-1] in [1, 2, 3, 4])

    return flag1

# check 2 lists and decide to vibrate
def decideNeg(list1,list2):
    flag= checkOneList_neg(list1) | checkOneList_neg(list2) # if any of them contain continious negative same emotion
    return flag

# decide if the emotions imbalance

# check 2 lists and decide to display