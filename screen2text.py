# screenshot the current screen and extract the text
# real time
# easyOCR is faster than keras,

import utility
import emoManager
from ferClf import predictEmo as preFaceEmo
import pytesseract
from PIL import ImageGrab
import numpy as np
import keyboard
import pickle
import serial.tools.list_ports


# import cv2

# test: read the text from one prepared image

# reader = easyocr.Reader(['en'])
# detector=keras_ocr.detection.Detector(
#     weights='clovaai_general', load_from_torch=False, optimizer='adam', backbone_name='vgg'
# )
# image = cv2.imread('t1.png', 1)
# result1=detector.detect(
#     image, detection_threshold=0.7, text_threshold=0.4, link_threshold=0.4, size_threshold=10,
# )
# half = cv2.resize(image, (0, 0), fx = 0.5, fy = 0.5)
# result = reader.readtext(image,detail=0,batch_size=2)# get rid of the meaningless numbers
# print(result)

#detect emotion from text
def predictTextEmo(OCRresult,clf):
    # extract feature
    toPredict = utility.cleanText(OCRresult)
    X = dictWords.transform([toPredict]).toarray()  # extract features from dictionary
    y_predicted = clf.predict(X)[0]
    emo_predicted = [k for k, v in utility.getEmoCode('').items() if v == y_predicted][0]  # convert back to emotion
    return y_predicted, emo_predicted

#detect emotion from facial expression
def predictFaceEmo(img,clf):
    y_predicted = preFaceEmo(img,clf)  # landmarks
    # detect face frame and crop the face part for HOG
    if (y_predicted!=None):
        emo_predicted = [k for k, v in utility.getEmoCode('').items() if v == y_predicted][0]
    else:
        emo_predicted = 'not detected'

    return y_predicted, emo_predicted

# recover trained model and dictionary as global variables
# recover text classifier
with open('NB_trained.pkl', 'rb') as load_data:
    clf_text = pickle.load(load_data)
#recover face classifier
with open('SVM_trained.pkl', 'rb') as load_clf:
    clf_face = pickle.load(load_clf)

# dictionary
with open('dict.pkl', 'rb') as load_data:
    dictWords = pickle.load(load_data)

#serial communication
plist = list(serial.tools.list_ports.comports())
if len(plist) <= 0:
    print('no port detected!')
else:
    plist_0 = list(plist[0])
    serialName = plist_0[0]
    serialFd = serial.Serial(serialName, 9600, timeout=60)

# screenshot every 2-4 seconds
emoList_text = []  # a record of emotions in digits from text
emoList_face=[]

while True:
    image = ImageGrab.grab()  # screenshot
    result = pytesseract.image_to_string(image)  # OCR, 't1.png'
    # print("OCR: "+result)
    # to be developped: if emotions are imbalance, break
    if keyboard.is_pressed('enter'):
        break
    else:
        # text emotion
        y_text, emo_text = predictTextEmo(result,clf_text)
        emoList_text.append(y_text)
        print("text emotion: " + emo_text)

        # utility.comArduino("0",plist)  # flag: "1"-vibrate; "0"->stop vibration
        serialFd.write("0".encode('utf-8'))

        #facial expression
        y_face, emo_face = predictFaceEmo(np.array(image),clf_face)
        if y_face!=None:
            emoList_text.append(y_face)
            print("facial expression: " + emo_face)

        # three continious negative same emotion
        flag1=emoManager.decideNeg(emoList_face,emoList_text)
        if flag1:
                serialFd.write("1".encode('utf-8'))
                print("continous negative emotion!")

# display emotion UI
