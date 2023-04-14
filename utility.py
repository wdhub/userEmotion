# frequently used functions
# clean text, extract feature from dictionary

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

def getEmoCode(choice):
    if choice=='KDEF':
        emoCode={'HA':0, 'SA':1, 'AN':2, 'AF':3, 'DI':4, 'SU':5} # convert the encoded file name to digit label
    else:
        emoCode={'joy':0, 'sadness':1, 'anger':2, 'fear':3, 'disgust':4, 'surprise':5}
    return emoCode
    # convert text label to digit

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

# convert text to features
# return X_train, X_test, dictionary
def freExtract(com_train,com_test):
    # get dictionary
    model = TfidfVectorizer(max_features=2500, min_df=7, max_df=0.8, stop_words=stopwords.words('english'))
    model = model.fit(com_train)
    # utility.saveData("freq_dict.pkl",model)
    # extract features
    X_train = model.transform(com_train).toarray()
    X_test = model.transform(com_test).toarray()

    return X_train,X_test,model