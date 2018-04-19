import numpy as np
import pandas as pd
import glob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score



train_path = "./aclImdb/" # use terminal to ls files under this directory
test_path = "./imdb_te.csv" # test data for grade evaluation

#train_path = "../resource/asnlib/public/aclImdb/" # use terminal to ls files under this directory
#test_path = "../resource/asnlib/public/imdb_te.csv" # test data for grade evaluation


# uncomment this before uploading the file
# train_path = "../resource/asnlib/public/aclImdb/train/" # use terminal to ls files under this directory
# test_path = "../resource/asnlib/public/imdb_te.csv" # test data for grade evaluation


def classfier(inpath="./", name="imdb_tr.csv", ngram=1, outfile="./output.txt", tfidf=False):

    #load vocablary
    #f = open(train_path + 'imdb.vocab', 'r')
    #vocab_words = list(f)
    #vocab_words = [w[:-1] for w in vocab_words]
    #f.close()


    #load train dataset
    data = pd.read_csv(inpath+name)

    train_data, val_data = train_test_split(data, test_size=0.1, random_state=32)

    if not tfidf:
        #vectorizer = CountVectorizer(vocabulary=vocab_words, stop_words='english', ngram_range=(ngram,ngram))
        vectorizer = CountVectorizer(stop_words='english', ngram_range=(ngram,ngram))
    else:
        #vectorizer = TfidfVectorizer(vocabulary=vocab_words, stop_words='english', ngram_range=(ngram,ngram))
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(ngram,ngram))

    X_train = vectorizer.fit_transform(train_data['text'].tolist())
    Y_train = train_data['polarity'].tolist()

    X_val = vectorizer.transform(val_data['text'].tolist())
    Y_val = val_data['polarity'].tolist()


    clf = SGDClassifier(loss='hinge', penalty='l2')

    clf.fit(X_train, Y_train)

    #check performance on validation set
    val_predict = clf.predict(X_val)

    train_predict = clf.predict(X_train)

    print ("Train Accracy={}".format(accuracy_score(Y_train, train_predict)))
    print ("Validation Accracy={}".format(accuracy_score(Y_val, val_predict)))

    # load test dataset
    test_data = pd.read_csv(test_path, encoding='ISO-8859-1')
    X_test = vectorizer.transform(test_data['text'].tolist())

    #predict
    test_predict = clf.predict(X_test)

    f = open(outfile, 'w')
    for item in test_predict:
        f.write("%d\n" % item)
    f.close()



def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    '''Implement this module to extract
	and combine text files under train_path directory into 
    imdb_tr.csv. Each text file in train_path should be stored 
    as a row in imdb_tr.csv. And imdb_tr.csv should have two 
    columns, "text" and label'''

    inpath += 'train/'
    f = open('./stopwords.en.txt', 'r')
    stopwords = list(f)
    stopwords = [w[:-1] for w in stopwords]
    f.close()

    # get texts with +ve sentiments
    comments=[]
    labels =[]
    for file in glob.glob(inpath+"pos/*.txt"):
        text_file = open(file, "r")
        line = text_file.read()

        # remove stopwords
        #line = ' '.join(filter(lambda x: x.lower() not in stopwords, line.split()))

        comments.append(line)
        labels.append(1)
        text_file.close()

    # get texts with -ve sentiments
    for file in glob.glob(inpath+"neg/*.txt"):
        text_file = open(file, "r")
        line = text_file.read()
        comments.append(line)
        labels.append(0)
        text_file.close()

    df = pd.DataFrame.from_dict({'text':comments, 'polarity':labels})
    df = df[['text','polarity']]

    df.to_csv(outpath+name)


if __name__ == "__main__":

    #imdb_data_preprocess(train_path)

    '''train a SGD classifier using unigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''
    classfier(inpath = "./", name = "imdb_tr.csv", ngram = 1, outfile="./unigram.output.txt", tfidf = False)

    '''train a SGD classifier using bigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''
    classfier(inpath = "./", name = "imdb_tr.csv", ngram = 2, outfile="./bigram.output.txt", tfidf = False)

    '''train a SGD classifier using unigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write 
    output to unigram.output.txt'''
    classfier(inpath = "./", name = "imdb_tr.csv", ngram = 1, outfile="./unigramtfidf.output.txt", tfidf = True)

    '''train a SGD classifier using bigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write 
    output to unigram.output.txt'''
    classfier(inpath = "./", name = "imdb_tr.csv", ngram = 2, outfile="./bigramtfidf.output.txt", tfidf = True)