import numpy as np
import random
import os

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

# pick first 10.000 tweets 
tweetfraction = tweetfraction[0:10000]
tweetcontent = tweetcontent[0:10000]

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
for i in range(0, 10000-1):
	if( len(features[i]) != len(features[0]) ):
		print("FATAL: Incosistent dimension!")


##pickle: save python object to file

# from sklearn.feature_extraction.text import TfidfTransformer
#
# tfidf = TfidfTransformer()
# print(tfidf.fit_transform(count.fit_transform(data)).toarray())

# from sklearn import svm
# clf = svm.SVC(gamma=0.001, C=100.)

from sklearn.neural_network import MLPClassifier

clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(8, 7), random_state=1)

clf.fit(features, labels)
#testdata = count.transform(["ich mag keine Autos", "ich mag Autos", "ich mag Himmel", "Anna mag keine Himmel",
#                            "ich mag keine Himmel"]).toarray()
#prediction = clf.predict(testdata)

print("EOF.")
