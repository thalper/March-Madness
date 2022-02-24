import numpy as np
from sklearn.datasets import load_breast_cancer, load_digits
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_blobs

import hw2_submission as hw2

import numpy as np
import os
import re
import string
import math
#ALL CODE BELOW TAKEN FROM NAIVE BAYES 473 HOMEWORK

DATA_DIR = 'enron'
target_names = ['ham', 'spam']

def get_data(DATA_DIR):
    data = []
    target = []

    # spam
    spam_files = os.listdir(os.path.join(DATA_DIR, 'spam'))
    for spam_file in spam_files:
        with open(os.path.join(DATA_DIR, 'spam', spam_file), encoding="latin-1") as f:
            data.append(f.read())
            target.append(1)

    # ham
    ham_files = os.listdir(os.path.join(DATA_DIR, 'ham'))
    for ham_file in ham_files:
        with open(os.path.join(DATA_DIR, 'ham', ham_file), encoding="latin-1") as f:
            data.append(f.read())
            target.append(0)

    return data, target

seed = 222
np.random.seed(seed)

data_cancer = load_breast_cancer()
X_train_cancer, X_test_cancer, y_train_cancer, y_test_cancer = train_test_split(data_cancer.data, data_cancer.target, test_size=0.33, random_state=seed)

data, target = get_data('spam_dataset')
X_train_spam, X_test_spam, y_train_spam, y_test_spam = train_test_split(data, target, test_size=0.33, random_state=seed)

def test_lr(X_train, X_test, y_train, y_test):
    lr = hw2.Logistic_Regression()
    lr.fit(X_train, y_train.reshape(-1,1))

    acc = np.mean(lr.predict(X_test) == y_test.reshape(-1,1))
    print('test accuracy (yours) : {:.3f}'.format(acc))
    
    LR = LogisticRegression(solver='liblinear')
    LR.fit(X_train, y_train)
    
    y_hat = LR.predict(X_test)
    acc_LR = (np.mean(y_hat == y_test))
    print('test accuracy (sklearn package): {:.3f}'.format(acc_LR))


def test_spam(X_train, X_test, y_train, y_test):
    nb = hw2.Spam_Naive_Bayes()
    nb.fit(X_train, y_train)
    acc = np.mean(nb.predict(X_test) == y_test)
    print('test accuracy (yours) : {:.3f}'.format(acc))
    
    
    
if __name__ == '__main__':
    print(' ######## Test Logistic Regression (Cancer) ######## ')
    test_lr(X_train_cancer, X_test_cancer, y_train_cancer, y_test_cancer)
    
    print(' ######## Test Naive Bayes (Spam) ######## ')
    test_spam(X_train_spam, X_test_spam, y_train_spam, y_test_spam)
    
    
    