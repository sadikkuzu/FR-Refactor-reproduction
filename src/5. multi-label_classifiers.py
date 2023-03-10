import six
import sys
sys.modules['sklearn.externals.six'] = six
# https://stackoverflow.com/a/62354885

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import hamming_loss, accuracy_score, precision_score, recall_score, f1_score, classification_report
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pyodbc
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re

from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier


df_text = pd.read_csv('./dataset/TextPreprocessed.csv', encoding='iso-8859-1')
# print(df_text.head())
df_tags = pd.read_csv('./dataset/Tag.csv', encoding='iso-8859-1')

num_classes = 14
grouped_tags = df_tags.groupby("Tag").size().reset_index(name='count')
most_common_tags = grouped_tags.nlargest(num_classes, columns="count")
df_tags.Tag = df_tags.Tag.apply(lambda tag : tag if tag in most_common_tags.Tag.values else None)
df_tags = df_tags.dropna()

counts = df_tags.Tag.value_counts()
firstlast = counts[:5].append(counts[-5:])
firstlast.reset_index(name="count")

# print(firstlast)

def tags_for_question(question_id):
    return df_tags[df_tags['Id'] == question_id].Tag.values

def add_tags_column(row):
    row['Tags'] = tags_for_question(row['Id'])
    return row

df_questions = df_text.apply(add_tags_column, axis=1)

multilabel_binarizer = MultiLabelBinarizer()
multilabel_binarizer.fit(df_questions.Tags)
Y = multilabel_binarizer.transform(df_questions.Tags)

count_vect = CountVectorizer()
X_counts = count_vect.fit_transform(df_questions.Text.values.astype('U'))

tfidf_transformer = TfidfTransformer()
X_tfidf = tfidf_transformer.fit_transform(X_counts)

ros = RandomOverSampler(random_state=9000)
X_tfidf_resampled, Y_tfidf_resampled = ros.fit_resample(X_tfidf, Y)

x_train_tfidf, x_test_tfidf, y_train_tfidf, y_test_tfidf = train_test_split(X_tfidf_resampled, Y_tfidf_resampled, test_size=0.2, random_state=9000)


def hamming_score(y_true, y_pred, normalize=True, sample_weight=None):
    print(y_true.shape[0])
    print(y_pred)

    acc_list = []
    for i in range(y_true.shape[0]):
        set_true = set(np.where(y_true[i])[0])
        set_pred = set(np.where(y_pred[i])[0])
        tmp_a = None
        if len(set_true) == 0 and len(set_pred) == 0:
            tmp_a = 1
        else:
            # tmp_a = len(set_true.union(set_pred))
            tmp_a = len(set_true.intersection(set_pred))/float(len(set_true.union(set_pred)) )
        acc_list.append(tmp_a)
    # print("acc_list:::")
    # print(acc_list)
    return np.mean(acc_list)

def print_score(y_pred, clf):
    print("Clf: ", clf.__class__.__name__)
    print("Hamming loss: {}".format(hamming_loss(y_test_tfidf, y_pred)))
    print("Hamming score: {}".format(hamming_score(y_test_tfidf, y_pred)))
    print('Subset accuracy: {0}'.format(accuracy_score(y_test_tfidf, y_pred, normalize=True, sample_weight=None)))
    print('Subset precision: {0}'.format(precision_score(y_test_tfidf, y_pred, average='samples')))
    print("---")

sgd = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=6, tol=None)
lr = LogisticRegression()
mn = MultinomialNB()
svm = LinearSVC()
# lstm = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
lstm = MLPClassifier(solver='lbfgs', alpha=1e-3, hidden_layer_sizes=(5, 2), random_state=42)
# https://scikit-learn.org/stable/modules/neural_networks_supervised.html

qwe = 1
for classifier in [svm, lr, mn, sgd, lstm]:
    print(qwe)
    qwe += 1
    clf = OneVsRestClassifier(classifier)
    clf.fit(x_train_tfidf, y_train_tfidf)
    y_pred = clf.predict(x_test_tfidf)
    print_score(y_pred, classifier)
    print(classification_report(y_test_tfidf, y_pred))