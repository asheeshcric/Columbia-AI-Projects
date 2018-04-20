from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer


import csv
import os
import pandas as pd




def imdb_data_preprocess(text):
    global set_stop_word
    replaced_text = text.replace('<br />', ' ')     # Remove chars with space
    chars = ".,?!;:-_/<>~`@#$%^&*()+=[]{}|\\\"\'"   # String used for removing punctuations
    for c in chars:
        replaced_text = replaced_text.replace(c, ' ')
    replaced_text_list = replaced_text.split()
    pText = ' '.join([w for w in replaced_text_list if w.lower() not in set_stop_word])

    return pText


def dataPreprocess(inpath, name):
    data_folders = ['pos/', 'neg/']
    out_file = open(name, 'w', encoding='utf-8', newline='')
    out_writer = csv.writer(out_file)
    out_writer.writerow(['', 'text', 'polarity'])
    i = -1
    for folder in data_folders:
        current_path = inpath + folder
        for r, d, fns in os.walk(current_path):
            for fn in fns:
                i = i + 1
                tk = fn.split('_')
                rating = tk[1].split('.')
                with open(current_path + fn, 'r', encoding="utf-8") as inp_file:
                    text = inp_file.read()
                pText = imdb_data_preprocess(text)
                out_writer.writerow([i, pText, int(int(rating[0]) > 5)])
    out_file.close()


def trainTDM(trainData, ngram, tfidf):
    global list_stop_word
    if tfidf:
        vectorizer = TfidfVectorizer(ngram_range=(1, ngram), stop_words=list_stop_word)
    else:
        vectorizer = CountVectorizer(ngram_range=(1, ngram), stop_words=list_stop_word)
    termDocMatrix = vectorizer.fit_transform(trainData['text'])
    vocabulary = vectorizer.vocabulary_
    clf = SGDClassifier(loss='hinge', penalty='l1')
    clf.fit(termDocMatrix, trainData['polarity'])

    return vocabulary, clf


def testTDM(test_data, ngram, vocabulary, clf, tfidf):
    global list_stop_word
    if tfidf:
        tf_vectorizer = TfidfVectorizer(ngram_range=(1, ngram), stop_words=list_stop_word, vocabulary=vocabulary)
    else:
        tf_vectorizer = CountVectorizer(ngram_range=(1, ngram), stop_words=list_stop_word, vocabulary=vocabulary)
    term_doc_matrix = tf_vectorizer.fit_transform(test_data['text'])
    result_list = clf.predict(term_doc_matrix)

    return result_list


def writeToFile(fn, result_list):
    with open(fn, 'w', newline='') as out_file:
        out_writer = csv.writer(out_file)
        for result in result_list:
            out_writer.writerow([result])


def start_program():
    global set_stop_word
    global list_stop_word

    train_path = "../resource/lib/publicdata/aclImdb/train/"  # use terminal to ls files under this directory
    test_path = "../resource/lib/publicdata/imdb_te.csv"  # test data for grade evaluation
    complete_train_path = "imdb_tr.csv"

    with open("stopwords.en.txt", 'r') as inputfile:
        list_stop_word = inputfile.read().splitlines()
    set_stop_word = set(list_stop_word)

    dataPreprocess(inpath=train_path, name=complete_train_path)
    trainData = pd.read_csv(complete_train_path, encoding="utf-8")
    testData = pd.read_csv(test_path, encoding="ISO-8859-1")
    testData['text'] = testData['text'].apply(imdb_data_preprocess)

    # Unigram Prediction
    vocabulary, clf = trainTDM(trainData, ngram=1, tfidf=False)
    result_list = testTDM(testData, ngram=1, vocabulary=vocabulary, clf=clf, tfidf=False)
    writeToFile("unigram.output.txt", result_list)


    # Bigram Prediction
    vocabulary, clf = trainTDM(trainData, ngram=2, tfidf=False)
    result_list = testTDM(testData, ngram=2, vocabulary=vocabulary, clf=clf, tfidf=False)
    # Print results
    writeToFile("bigram.output.txt", result_list)



    # Unigram with Tfidf Prediction
    vocabulary, clf = trainTDM(trainData, ngram=1, tfidf=True)
    result_list = testTDM(testData, ngram=1, vocabulary=vocabulary, clf=clf, tfidf=True)
    writeToFile("unigramtfidf.output.txt", result_list)



    # Bigram with Tfidf Prediction
    vocabulary, clf = trainTDM(trainData, ngram=2, tfidf=True)
    result_list = testTDM(testData, ngram=2, vocabulary=vocabulary, clf=clf, tfidf=True)
    # Print results
    writeToFile("bigramtfidf.output.txt", result_list)
    # ---------------------------------#


if __name__ == "__main__":
    start_program()