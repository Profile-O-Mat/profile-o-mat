import numpy as np
import random
import os

DATA_SIZE = 10000
ITERATIONS = 1
ALPHA = 2e-6
LAYER = (500, 100)

tweetfraction = []
tweetcontent = []
# tweets = np.empty((0,2))

# read files
for fraction in os.listdir("../training_data/" + "partys/"):
    for account in os.listdir("../training_data/" + "partys/" + fraction):
        for id in os.listdir("../training_data/" + "partys/" + fraction + "/" + account + "/"):
            file = open("../training_data/" + "partys/" + fraction + "/" + account + "/" + id, 'r')
            # tweets = np.append(tweets, [fraction, file.read()])
            tweetfraction.append(fraction)
            tweetcontent.append(file.read())

            file.close()

print("Finished reading")

# shuffle data
shuffler = list(zip(tweetfraction, tweetcontent))
random.shuffle(shuffler)
tweetfraction, tweetcontent = zip(*shuffler)

# pick first DATA_SIZE tweets 
tweetfraction = tweetfraction[0:DATA_SIZE]
tweetcontent = tweetcontent[0:DATA_SIZE]

from sklearn.feature_extraction.text import CountVectorizer

# Create Bag-Of-Words
count = CountVectorizer()
data = np.asarray(tweetcontent)
features = count.fit_transform(data).toarray()

#select unique fractions
labels = []
fractionset = set(tweetfraction)
fractions = dict()
i = 0
for fraction in fractionset:
	fractions.update({fraction: i})
	i += 1

for fraction in tweetfraction:
	labels.append(fractions[fraction])

print("Got " + str(len(features)) + " training entrys")
print("Got " + str(len(labels)) + " labels")
print("Got " + str(len(features[0])) + " units long word bag")

# Check for consistent map [DEBUG]
for i in range(0, DATA_SIZE-1):
	if( len(features[i]) != len(features[0]) ):
		print("FATAL: Incosistent dimension!")


##pickle: save python object to file

# from sklearn.feature_extraction.text import TfidfTransformer
#
# tfidf = TfidfTransformer()
# print(tfidf.fit_transform(count.fit_transform(data)).toarray())

# from sklearn import svm
# clf = svm.SVC(gamma=0.001, C=100.)

print("Data is ready!")

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.33, random_state=42)

print("Creating ANN...")
clf = MLPClassifier(solver='lbfgs', activation='tanh', alpha=ALPHA, hidden_layer_sizes=LAYER, random_state=1, max_iter=ITERATIONS, verbose=True)

print("Training ANN (max. " + str(ITERATIONS) + " itr.)...")
clf.fit(X_train, y_train)

predictions = clf.predict(X_test)
error = np.mean( predictions != y_test )

print("Test error: " + str(error))

print("Exporting data structures:")

import pickle

print(" -> CountVectorizer")
with open("export_count.dat", "wb+") as handle:
	pickle.dump(count, handle)

print(" -> MLPClassifier")
with open("export_clf.dat", "wb+") as handle:
	pickle.dump(clf, handle)

print(" -> Fractions")
with open("export_fractions.dat", "wb+") as handle:
	pickle.dump(fractions, handle)

print("EOF!")
