import collections
import math
import numpy as np
import re
import string

#file for creating AI (naive Bayes, etc) for creating weights for later simulation
def createWeights():
    numWeights = 24 # 
    weights = [0.5]*numWeights  # initialization before we do Naive Bayes analysis
    temp = w3pta(12, weights[0], 8, weights[1])
    return weights 

def w3pta(Ataken, wAT, Ballowed, WBA):
    return Ataken*wAT + Ballowed*WBA

#ALL CODE BELOW TAKEN FROM NAIVE BAYES 473 HOMEWORK
class Logistic_Regression():
    def __init__(self):
        self.W = None
        self.b = None

    def fit(self, x, y, batch_size=64, iteration=2000, learning_rate=1e-2):
        """
        Train this Logistic Regression classifier using mini-batch stochastic gradient descent.
        Inputs:
        - X: A numpy array of shape (N, D) containing training data; there are N
          training samples each of dimension D.
        - y: A numpy array of shape (N,) containing training labels; y[i] = c
          means that X[i] has label 0 <= c < C for C classes.
        - learning_rate: (float) learning rate for optimization.
        - iteration: (integer) number of steps to take when optimizing
        - batch_size: (integer) number of training examples to use at each step.

        Use the given learning_rate, iteration, or batch_size for this homework problem.

        Returns:
        None
        """
        dim = x.shape[1]
        num_train = x.shape[0]

        # initialize W
        if self.W == None:
            self.W = 0.001 * np.random.randn(dim, 1)
            self.b = 0

        for it in range(1, iteration + 1):
            batch_ind = np.random.choice(num_train, batch_size)

            x_batch = x[batch_ind]
            y_batch = y[batch_ind]

            ############################################################
            ############################################################
            # BEGIN_YOUR_CODE
            # Calculate loss and update W, b
            y_pred = self.predict(x_batch)
            loss, gradient = self.loss(x_batch, y_pred, y_batch)

            self.W -= learning_rate * gradient['dW']
            self.b -= learning_rate * gradient['db']

            acc = np.mean(y_pred == y_batch)
            pass;

            # END_YOUR_CODE
            ############################################################
            ############################################################
            if it % 50 == 0:
                print('iteration %d / %d: accuracy : %f: loss : %f' % (it, iteration, acc, loss))

    def predict(self, x):
        """
        Use the trained weights of this linear classifier to predict labels for
        data points.
        Inputs:

        Returns:
        - y_pred: Predicted labels for the data in X. y_pred is a 1-dimensional
          array of length N, and each element is an integer giving the predicted
          class.
        """
        ############################################################
        ############################################################
        # BEGIN_YOUR_CODE
        # Calculate predicted y
        y_pred = []
        z = x.dot(self.W)
        sig = self.sigmoid(z)
        i = 0
        while i < len(sig):
            if sig[i] >= 0.5:
                sig[i] = 1
            else:
                sig[i] = 0
            y_pred.append(sig[i])
            i += 1
        pass;

        # END_YOUR_CODE
        ############################################################
        ############################################################
        return y_pred

    def loss(self, x_batch, y_pred, y_batch):
        """
        Compute the loss function and its derivative.
        Inputs:
        - X_batch: A numpy array of shape (N, D) containing a minibatch of N
          data points; each point has dimension D.
        - y_batch: A numpy array of shape (N,) containing labels for the minibatch.

        Returns: A tuple containing:
        - loss as a single float
        - gradient dictionary with two keys : 'dW' and 'db'
        """
        gradient = {'dW': None, 'db': None}
        ############################################################
        ############################################################
        # BEGIN_YOUR_CODE
        # Calculate loss and gradient
        loss = 0
        i = 0
        while i < len(y_pred):
            loss += y_batch[i] * math.log(y_pred[i] + 1e-5) - (1 - y_batch[i]) * math.log(1 - y_pred[i] + 1e-5)
            i += 1
        loss = -1 / len(y_pred) * loss
        gradient['dW'] = (x_batch.T).dot(y_pred - y_batch)
        gradient['db'] = y_pred - y_batch
        pass;

        # END_YOUR_CODE
        ############################################################
        ############################################################
        return loss, gradient

    def sigmoid(self, z):
        """
        Compute the sigmoid of z
        Inputs:
        z : A scalar or numpy array of any size.
        Return:
        s : sigmoid of input
        """
        ############################################################
        ############################################################
        # BEGIN_YOUR_CODE
        # Calculate loss and update W
        z = np.clip(z, -1, None)
        s = 1 / (1 + np.exp(-z))
        pass;

        # END_YOUR_CODE
        ############################################################
        ############################################################

        return s


class Spam_Naive_Bayes(object):
    """Implementation of Naive Bayes for Spam detection."""
    #THIS NEEDS TO BE CHANGED FOR TEAM COMPARISONS, NOT EMAILS
    def clean(self, s):
        translator = str.maketrans("", "", string.punctuation)
        return s.translate(translator)

    def tokenize(self, text):
        text = self.clean(text).lower()
        return re.split("\W+", text)

    def get_word_counts(self, words):
        """
        Generate a dictionary 'word_counts'
        Hint: You can use helper function self.clean and self.toeknize.
              self.tokenize(x) can generate a list of words in an email x.

        Inputs:
            -words : list of words that is used in a data sample
        Output:
            -word_counts : contains each word as a key and number of that word is used from input words.
        """
        ############################################################
        ############################################################
        # BEGIN_YOUR_CODE
        # calculate naive bayes probability of each class of input x
        words = self.clean(words)
        token = self.tokenize(words)
        word_counts = {}
        for i in token:
            if i in word_counts:
                word_counts[i] += 1
            else:
                word_counts.update({i: 1})
        pass
        # END_YOUR_CODE
        ############################################################
        ############################################################

        return word_counts

    def fit(self, X_train, y_train):
        """
        compute likelihood of all words given a class

        Inputs:
            -X_train : list of emails
            -y_train : list of target label (spam : 1, non-spam : 0)

        Variables:
            -self.num_messages : dictionary contains number of data that is spam or not
            -self.word_counts : dictionary counts the number of certain word in class 'spam' and 'ham'.
            -self.class_priors : dictionary of prior probability of class 'spam' and 'ham'.
        Output:
            None
        """
        ############################################################
        ############################################################
        # BEGIN_YOUR_CODE
        # calculate naive bayes probability of each class of input x
        self.num_messages = {}
        self.word_counts = {}
        self.class_priors = {}
        i = 0
        j = 0
        wordSpam = {}
        wordHam = {}
        for x, y in zip(X_train, y_train):
            words = self.get_word_counts(x)
            if y == 0:
                i += 1
                self.num_messages.update({'ham': i})
                for key, val in zip(words.keys(), words.values()):
                    if key in wordHam:
                        wordHam[key] += words[key]
                    else:
                        wordHam.update({key: val})
            else:
                j += 1
                self.num_messages.update({'spam': j})
                for key, val in zip(words.keys(), words.values()):
                    if key in wordSpam:
                        wordSpam[key] += words[key]
                    else:
                        wordSpam.update({key: val})
        self.word_counts.update({'spam': wordSpam})
        self.word_counts.update({'ham': wordHam})
        self.class_priors['spam'] = self.num_messages['spam'] / (self.num_messages['spam'] + self.num_messages['ham'])
        self.class_priors['ham'] = self.num_messages['ham'] / (self.num_messages['spam'] + self.num_messages['ham'])
        pass
        # END_YOUR_CODE
        ############################################################
        ############################################################

    def predict(self, X):
        """
        predict that input X is spam of not.
        Given a set of words {x_i}, for x_i in an email(x), if the likelihood

        p(x_0|spam) * p(x_1|spam) * ... * p(x_n|spam) * y(spam) > p(x_0|ham) * p(x_1|ham) * ... * p(x_n|ham) * y(ham),

        then, the email would be spam.

        Inputs:
            -X : list of emails

        Output:
            -result : A numpy array of shape (N,). It should tell rather a mail is spam(1) or not(0).
        """

        result = []
        for x in X:
            ############################################################
            ############################################################
            # BEGIN_YOUR_CODE
            # calculate naive bayes probability of each class of input x
            words = self.get_word_counts(x)
            spamProb = math.log(self.class_priors['spam'])
            hamProb = math.log(self.class_priors['ham'])
            for key in words.keys():
                tot = 0
                if key in self.word_counts['spam']:
                    tot += 1
                if key in self.word_counts['ham']:
                    tot += 1
                if tot == 2:
                    spamProb += math.log(
                        self.word_counts['spam'][key] / (self.word_counts['spam'][key] + self.word_counts['ham'][key]))
                    hamProb += math.log(
                        self.word_counts['ham'][key] / (self.word_counts['spam'][key] + self.word_counts['ham'][key]))
            if spamProb > hamProb:
                result.append(1)
            else:
                result.append(0)
            pass
            # END_YOUR_CODE
            ############################################################
            ############################################################
        result = np.array(result)
        return result