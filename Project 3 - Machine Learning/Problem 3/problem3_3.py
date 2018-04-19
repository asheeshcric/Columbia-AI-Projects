import csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import sklearn.neighbors
from sklearn import tree
import sys


arr_data = []
arr_target = []
input_csv = csv.reader(open(sys.argv[1], newline=''), delimiter=',')
output_csv = csv.writer(open(sys.argv[2], 'w', newline=''), delimiter=',')

for line in input_csv:
    if ('A' in line or 'B' in line or 'label' in line):
        continue
    arr_data.append([float(line[0]), float(line[1])])
    arr_target.append(float(line[2]))


# SVM with Linear Kernel
values = [{'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'kernel': ['linear']}]
X_train, X_test, Y_train, Y_test = train_test_split(arr_data, arr_target, test_size=0.4, random_state=0)
clf = GridSearchCV(estimator=svm.SVC(), param_grid=values, cv=5, scoring='accuracy')
clf.fit(X_train, Y_train)
output_csv.writerow(['svm_linear', clf.best_score_, clf.score(X_test, Y_test)])

# SVM with Polynomial Kernel
values = [{'C': [0.1, 1, 3], 'kernel': ['poly'], 'degree': [4, 5, 6], 'gamma': [0.1, 0.5]}]
X_train, X_test, Y_train, Y_test = train_test_split(arr_data, arr_target, test_size=0.4, random_state=0)
clf = GridSearchCV(estimator=svm.SVC(), param_grid=values, cv=5, scoring='accuracy')
clf.fit(X_train, Y_train)
output_csv.writerow(['svm_polynomial', clf.best_score_, clf.score(X_test, Y_test)])

# SVM with RBF Kernel
values = [{'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'kernel': ['rbf'], 'gamma': [0.1, 0.5, 1, 3, 6, 10]}]
X_train, X_test, Y_train, Y_test = train_test_split(arr_data, arr_target, test_size=0.4, random_state=0)
clf = GridSearchCV(estimator=svm.SVC(), param_grid=values, cv=5, scoring='accuracy')
clf.fit(X_train, Y_train)
output_csv.writerow(['svm_rbf', clf.best_score_, clf.score(X_test, Y_test)])

# Logistic Regression
values = [{'C': [0.1, 0.5, 1, 5, 10, 50, 100]}]
X_train, X_test, Y_train, Y_test = train_test_split(arr_data, arr_target, test_size=0.4, random_state=0)
clf = GridSearchCV(estimator=LogisticRegression(), param_grid=values, cv=5, scoring='accuracy')
clf.fit(X_train, Y_train)
output_csv.writerow(['logistic', clf.best_score_, clf.score(X_test, Y_test)])

# k-Nearest Neighbors
values = [{'n_neighbors': range(1, 51), 'leaf_size': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]}]
X_train, X_test, Y_train, Y_test = train_test_split(arr_data, arr_target, test_size=0.4, random_state=0)
clf = GridSearchCV(sklearn.neighbors.KNeighborsClassifier(), param_grid=values, cv=5, scoring='accuracy')
clf.fit(X_train, Y_train)
output_csv.writerow(['knn', clf.best_score_, clf.score(X_test, Y_test)])

# Decision Trees
values = [{'max_depth': range(1, 51), 'min_samples_split': range(2, 11)}]
X_train, X_test, Y_train, Y_test = train_test_split(arr_data, arr_target, test_size=0.4, random_state=0)
clf = GridSearchCV(tree.DecisionTreeClassifier(), param_grid=values, cv=5, scoring='accuracy')
clf.fit(X_train, Y_train)
output_csv.writerow(['decision_tree', clf.best_score_, clf.score(X_test, Y_test)])

# Random Forest
values = [{'max_depth': range(1, 51), 'min_samples_split': range(2, 11)}]
X_train, X_test, Y_train, Y_test = train_test_split(arr_data, arr_target, test_size=0.4, random_state=0)
clf = GridSearchCV(RandomForestClassifier(), param_grid=values, cv=5, scoring='accuracy')
clf.fit(X_train, Y_train)
output_csv.writerow(['random_forest', clf.best_score_, clf.score(X_test, Y_test)])
