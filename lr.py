#!/usr/bin/env python

import sys

import numpy as np
from sklearn import linear_model, metrics
from matplotlib import pyplot as plt

C_LST = [0.001,0.01,0.1,1.0,2.0]
TOL = 0.00001
D = 658
K = 10


def main():
    base_name = sys.argv[1]
    
    data_train = np.load('./data_train.npy')
    data_test = np.load('./data_test.npy')
    X_train = data_train[:, 0:-1]
    Y_train = data_train[:, -1]
    X_test = data_test[:, 0:-1]
    Y_test = data_test[:, -1]
    
    model = linear_model.LogisticRegressionCV(cv=K, Cs=C_LST, penalty='l2', dual=False, tol=TOL, verbose=1)
    model.fit(X_train, Y_train)
    
    Y_test_proba = model.predict_proba(X_test)[:, 1]
    accuracy = model.score(X_test, Y_test)
    auc = metrics.roc_auc_score(Y_test, Y_test_proba)
    fpr, tpr, thresholds = metrics.roc_curve(Y_test, Y_test_proba)
    
    np.save(base_name + '_fpr.npy', fpr)
    np.save(base_name + '_tpr.npy', tpr)
    outfile = open(base_name + '_results.txt', 'w')
    outfile.write('accuracy\t' + str(accuracy) + '\n')
    outfile.write('AUC\t' + str(auc) + '\n')
    outfile.close()
    
#     plt.figure(figsize=(10, 8))
#     plt.plot(fpr, tpr, 'b.')
#     plt.title('Logistic regression; accuracy = %.1f%%; AUC = %.3f' % (accuracy*100, auc))
#     plt.xlabel('False Positive Rate')
#     plt.ylabel('True Positive Rate')
#     plt.xlim((0, 1))
#     plt.ylim((0, 1))
#     plt.show()
    
if __name__ == '__main__':
    main()
