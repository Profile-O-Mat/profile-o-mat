###
### Highly experimental version
###

import numpy as np
import random
import os

DATA_SIZE = 10000
ITERATIONS = 1
LAYER = ()

###
### load data
###
tweetfraction = []
tweetcontent = []
# tweets = np.empty((0,2))

# read files
for fraction in os.listdir("../training_data/" + "partys/"):
    print("Reading..." + fraction)
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

data_row = np.asarray(tweetcontent)

###
### Vectorize input
###
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# Create Bag-Of-Words
count_vect = CountVectorizer()
data_counts = count_vect.fit_transform(data_row)
print("Word bag: " + str(data_counts.shape))

# Create term frequency times inverse document frequency (tf-idf)
tf_transformer = TfidfTransformer()
data_tf = tf_transformer.fit_transform(data_counts)
print("Tf data: " + str(data_tf.shape))

features = data_tf.toarray()


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

# Verbose
print("Got " + str(len(features)) + " training entrys")
print("Got " + str(len(labels)) + " labels")
print("Got " + str(len(features[0])) + " units long tfidf vectors")

# Check for consistent map [DEBUG]
for i in range(0, DATA_SIZE-1):
	if( len(features[i]) != len(features[0]) ):
		print("FATAL: Incosistent dimension!")

print("Data is ready!")


###
### Train MLPclassifier
###
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# Take 33% of the data for testing
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.33, random_state=42)

# Note that another 10% of the taining data is used as validation data for early_stopping
# Doing so allows the usage of an adaptive learning rate

print("Creating MLPClassifier...")
clf = MLPClassifier(solver='sgd', activation='tanh', learning_rate='adaptive', early_stopping=True,
					hidden_layer_sizes=LAYER, random_state=1, max_iter=ITERATIONS, verbose=True)

print("Training ANN (max. " + str(ITERATIONS) + " itr.)...")
clf.fit(X_train, y_train)

###
### Evaluating performance
###
from sklearn import metrics

# Naive test error
print("Predicting test data...")
predictions = clf.predict(X_test)
error = np.mean( predictions != y_test )

print("Test error: " + str(error))

# Advanced performance analzsis
print(metrics.classification_report(y_test, predictions, target_names=list(fractionset)))


###
### Export data
###
import pickle

print("Exporting data structures:")

print(" -> CountVectorizer")
with open("export_count.dat", "wb+") as handle:
	pickle.dump(count, handle)

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
