# facial expression classifier
# features: HOG in window, landmark
# model: SVM
# Dataset: The Karolinska Directed Emotional Faces
# landmark model: http://dlib.net/face_landmark_detection.py.html
# Problem to be solved: HOG feature vector can be different in length due to different sizes of images
# Possible solution: find the same-sized rectangle of face and then calculate HOG

import numpy as np
import os
import dlib
import cv2
from skimage.feature import hog
import utility
import pickle
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

# prepare models
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


# find landmark feature in the given image
def findLM(img):
    detected = detector(img, 1)
    # only test the first face
    if (len(detected) != 0):  # face is detected
        shape = predictor(img, detected[0])
        point2array = np.array([[p.x, p.y] for p in shape.parts()])  # convert points to array
        landmark = point2array.flatten()  # convert array to vector
    else:
        landmark = np.zeros([136])  # 68 points->vector dimention: 136
        print("Warning: face not detected!")
    return landmark


# calculate HOG of an image
def calHOG(img):
    # HOG
    imGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # resize to 0.2
    h = int(imGray.shape[0] * 0.2)
    w = int(imGray.shape[1] * 0.2)
    imResize = cv2.resize(imGray, (h, w))

    HOG = hog(imResize, orientations=8, pixels_per_cell=[16, 16],
              cells_per_block=[2, 2],
              feature_vector=True
              )

    return HOG


# def sliding_hog_windows(img):
#     hog_windows = []
#     imGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     h= int(imGray.shape[0]*0.2)
#     w = int(imGray.shape[1] * 0.2)
#     imResize=cv2.resize(imGray,(h,w))
#     for y in range(0, w, window_step):
#         for x in range(0, h, window_step):
#             window = imResize[y:y+window_size, x:x+window_size]
#             hog_windows.extend(hog(window, orientations=8, pixels_per_cell=(8, 8),
#                                             cells_per_block=(1, 1)))
#     return hog_windows

# extract features for training and evaluation
filePath = os.getcwd() + '/KDEF'
fea_lm = []
fea_HOG = []
labels = []
countFolder = 0
for subPath in os.listdir(filePath):
    for filename in os.listdir(filePath + '/' + subPath):
        img = cv2.imread(filePath + '/' + subPath + '/' + filename)  # test: 'KDEF/AF01/AF01AFFL.JPG'

        # assign labels
        emoMark = filename[4:6]
        # don't use neutral
        if (emoMark != 'NE'):
            label = utility.getEmoCode(choice='KDEF')[emoMark]

            # calculate features
            landmark = findLM(img)
            if landmark.sum() != 0.0:  # if face is detected count this sample
                HOG = calHOG(img)
                fea_lm.append(landmark)
                fea_HOG.append(HOG)
                labels.append(label)

            print("feature extraction done: " + subPath + '/' + filename)

    # save every five folders
    countFolder += 1
    if countFolder % 5 == 0:
        # save middle results
        with open('fea_HOG.pkl', "wb") as file:
            pickle.dump(fea_HOG, file, True)
        with open('fea_LM.pkl', "wb") as file:
            pickle.dump(fea_lm, file, True)
        print("feature saved: " + subPath)

#combine features
fea_lm_HOG=[]
for lll,hhh in zip(fea_lm,fea_HOG):
    fea_lm_HOG.append(np.hstack((lll,hhh)))

# train SVM
fea=fea_lm_HOG
X_train, X_test, y_train, y_test = train_test_split(fea, labels, test_size=0.25)
clf = SVC(kernel='linear', C=0.1, gamma='auto')
clf.fit(X_train, y_train)
# evaluate
y_test_predicted = clf.predict(X_test)
score = accuracy_score(y_test, y_test_predicted)
confusion = confusion_matrix(y_test, y_test_predicted, normalize='true')

#predict
img = cv2.imread('t2_f.png')
img=cv2.resize(img,(762,562))
landmark = findLM(img)
HOG = calHOG(img)
x=np.hstack((landmark,HOG)).reshape(1, -1)
clf.predict(x)