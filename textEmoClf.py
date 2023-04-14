# train emotion classifier
# predict
# dataset: TEC, http://saifmohammad.com/WebPages/SentimentEmotionLabeledData.html

import re
import utility
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import numpy as np
import pytesseract



# read and sort dataset

# read dataset

f=open('Jan9-2012-tweets-clean.txt',encoding='utf-8')
data = f.readlines()
f.close()

#sort dataset into samples and labels
tweets=[]
labels=[]

for ddd in data:
    tweet = re.findall(r".*\t(.*)\t",ddd)[0] #the result is a list so we take the first element
    label= re.findall(r".*:: (.*)\n",ddd)[0]
    tweets.append(utility.cleanText(tweet))
    labels.append(utility.getEmoCode(choice='')[label])

# generate dictionary

#split training and evaluation set
com_train,com_test, y_train, y_test = train_test_split(tweets,labels,test_size=0.25)
X_train,X_test,dictWords=utility.freExtract(com_train,com_test)

# train classifier
#weighted Bayesian, sample_weight
c_w = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
sample_weight=[c_w[i] for i in y_train]
sample_weight=np.array(sample_weight)

# y_train=y_train.astype('int')
clf=MultinomialNB().fit(X_train,y_train,sample_weight)

# evaluate
y_test_predicted=clf.predict(X_test)
score=accuracy_score(y_test, y_test_predicted)
confusion=confusion_matrix(y_test, y_test_predicted,normalize='true')

# predict
result=pytesseract.image_to_string('t1.png')
toPredict=utility.cleanText(result)
X = dictWords.transform([toPredict]).toarray() # extract features from dictionary
y_predicted=clf.predict(X)[0]
emo_predicted=[k for k, v in utility.getEmoCode(choice='').items() if v == y_predicted][0] # convert back to emotion

