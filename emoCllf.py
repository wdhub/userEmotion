# train emotion classifier
# predict
# dataset: TEC, http://saifmohammad.com/WebPages/SentimentEmotionLabeledData.html

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# functions
def cleanText(comment):
    # twits-specific cleaning: mention, quote symbol & html
    noMention = re.sub("@[A-Za-z0-9]+", "", comment)  # mention
    noQuot = re.sub("&quot;", "", noMention)  # no quote symbol
    # HTML
    temp = re.sub(r'^(https:\S+)', ' ', noQuot)
    noHTML = re.sub(r'[a-zA-Z]+://[^\s]*', '', temp)

    # clean single characters, spaces, transform to lowercase
    noSpecial = re.sub(r'\W', ' ', noHTML)  # Remove all the special characters
    # single characters
    noSingle = re.sub(r'\s+[a-zA-Z]\s+', ' ', noSpecial)
    noSingle = re.sub(r'\^[a-zA-Z]\s+', ' ', noSingle)
    # space
    oneSpace = re.sub(r'\s+', ' ', noSingle, flags=re.I)  # Substitute multiple spaces with single space
    noEndSpace = oneSpace.strip()  # first and last space
    cleared = noEndSpace.lower()  # Convert to Lowercase

    return cleared

def freExtract(com_train,com_test):
    # get dictionary
    model = TfidfVectorizer(max_features=2500, min_df=7, max_df=0.8, stop_words=stopwords.words('english'))
    model = model.fit(com_train)
    # utility.saveData("freq_dict.pkl",model)
    # extract features
    X_train = model.transform(com_train).toarray()
    X_test = model.transform(com_test).toarray()

    return X_train,X_test

# read and sort dataset

# read dataset

f=open('Jan9-2012-tweets-clean.txt',encoding='utf-8')
data = f.readlines()
f.close()

#sort dataset into samples and labels
tweets=[]
labels=[]
emoCode={'joy':0, 'sadness':1, 'anger':2, 'fear':3, 'disgust':4, 'surprise':5} # convert text label to digit
for ddd in data:
    tweet = re.findall(r".*\t(.*)\t",ddd)[0] #the result is a list so we take the first element
    label= re.findall(r".*:: (.*)\n",ddd)[0]
    tweets.append(cleanText(tweet))
    labels.append(emoCode[label])

# generate dictionary

#split training and evaluation set
com_train,com_test, y_train, y_test = train_test_split(tweets,labels,test_size=0.25)
X_train,X_test=freExtract(com_train,com_test)

# train classifier
y_train=y_train.astype('int')
clf=MultinomialNB().fit(X_train,y_train)

# evaluate
score=accuracy_score(y_test, clf.predict(X_test))


# predict


