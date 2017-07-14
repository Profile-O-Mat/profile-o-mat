#####################
### Visualization ###
#####################
import itertools
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, round(cm[i, j], 3),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


######################
### Training logic ###
######################
import numpy as np
import random
import os

DATA_SIZE = 200000
L2_PENALTY = 1e-3
LEARNING_RATE_INIT = 1e-3
ITERATIONS = 500
LAYER = (1000, 500, 500)
SOLVER = "adam" # adam and lbfgs are recommended
TEST_SIZE = 1/3


###
### load data
###
tweetfraction = []
tweetcontent = []
# tweets = np.empty((0,2))

# read files
for fraction in os.listdir("../training_data/" + "partys/"):
	print("Reading " + fraction + "... ", end='')
	for account in os.listdir("../training_data/" + "partys/" + fraction):
		for id in os.listdir("../training_data/" + "partys/" + fraction + "/" + account + "/"):
			file = open("../training_data/" + "partys/" + fraction + "/" + account + "/" + id, 'r')
			# tweets = np.append(tweets, [fraction, file.read()])
			tweetfraction.append(fraction)
			tweetcontent.append(file.read())

			file.close()
	print("OK!")

print("Finished reading: ", end='')

# shuffle data
shuffler = list(zip(tweetfraction, tweetcontent))
random.shuffle(shuffler)
tweetfraction, tweetcontent = zip(*shuffler)

# pick first DATA_SIZE tweets
DATA_SIZE = min(DATA_SIZE, len(tweetfraction))
tweetfraction = tweetfraction[0:DATA_SIZE]
tweetcontent = tweetcontent[0:DATA_SIZE]

data_raw = np.asarray(tweetcontent)
print(str(len(data_raw)) + " tweets loaded!")


###
### Vectorize input
###
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# Create Bag-Of-Words
print("\nFitting CountVectorizer... ", end='')
count_vect = CountVectorizer()
data_counts = count_vect.fit_transform(data_raw)
print("OK!")

# Create term frequency times inverse document frequency (tf-idf)
print("Fitting Tfidf-Vectorizer... ", end='')
tf_transformer = TfidfTransformer()
data_tf = tf_transformer.fit_transform(data_counts)
print("OK, final data shape: " + str(data_tf.shape))


###
### Convert fractions from str to int
###
labels = []
fractionset = set(tweetfraction) # get unique fractions
fractions = dict() # prepare dictionary
i = 0
for fraction in fractionset: # iterate over unique entrys
	fractions.update({fraction: i}) # insert new dict entry str -> int
	i += 1

for fraction in tweetfraction: 
	labels.append(fractions[fraction]) # change entry in original dataset to int classes

print("Data is ready!")


###
### Train MLPclassifier
###
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# Take 33% of the data for testing
X_train, X_test, y_train, y_test = train_test_split(data_tf, labels, test_size=TEST_SIZE, random_state=42)

# Note that another 10% of the taining data is used as validation data for early_stopping
# Doing so allows the usage of an adaptive learning rate

print("Creating MLPClassifier...")
clf = MLPClassifier(solver=SOLVER, activation='tanh', verbose=True, early_stopping=False,
					hidden_layer_sizes=LAYER, max_iter=ITERATIONS, alpha=L2_PENALTY, learning_rate_init=LEARNING_RATE_INIT)

print("Training ANN (max. " + str(ITERATIONS) + " itr.)...")
clf.fit(X_train, y_train)


###
### Evaluating performance
###
from sklearn import metrics

# Naive test error
print("Evaluating performance...")
print("Evaluating performance...", file=open("evaluation.txt", "w"))
p_train = clf.predict(X_train)
p_test = clf.predict(X_test)
e_train = np.mean( p_train != y_train )
e_test = np.mean( p_test != y_test )

print("Training error: " + str(e_train))
print("Training error: " + str(e_train), file=open("evaluation.txt", "a"))
print("Test error: " + str(e_test))
print("Test error: " + str(e_test), file=open("evaluation.txt", "a"))

# Advanced performance analzsis
print("\nTraining data:")
print("\nTraining data:", file=open("evaluation.txt", "a"))
print(metrics.classification_report(y_train, p_train, target_names=list(fractionset)))
print(metrics.classification_report(y_train, p_train, target_names=list(fractionset)), file=open("evaluation.txt", "a"))
print("\nTest data:")
print("\nTest data:", file=open("evaluation.txt", "a"))
print(metrics.classification_report(y_test, p_test, target_names=list(fractionset)))
print(metrics.classification_report(y_test, p_test, target_names=list(fractionset)), file=open("evaluation.txt", "a"))

# Compute confusion matrix
cnf_matrix = confusion_matrix(y_test, p_test)
np.set_printoptions(precision=2)

# Plot normalized confusion matrix
print("Creating confusion matrix...") 
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=list(fractionset), normalize=True,
                      title='Normalized confusion matrix (test data)')

plt.savefig("confuson.png")


###
### Export data
###
import pickle

print("\nExporting data structures:")

print(" -> CountVectorizer")
with open("export_count.dat", "wb+") as handle:
	pickle.dump(count_vect, handle)

print(" -> Tf-idf Transformer")
with open("export_tfidf.dat", "wb+") as handle:
	pickle.dump(tf_transformer, handle)

print(" -> MLPClassifier")
with open("export_clf.dat", "wb+") as handle:
	pickle.dump(clf, handle)

print(" -> Fractions")
with open("export_fractions.dat", "wb+") as handle:
	pickle.dump(fractions, handle)

print("EOF!")
