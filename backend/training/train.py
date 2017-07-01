import numpy as np

import os

tweetfraction = []
tweetcontent = []
# tweets = np.empty((0,2))

for fraction in os.listdir("../training_data/" + "partys/"):
    for account in os.listdir("../training_data/" + "partys/" + fraction):
        for id in os.listdir("../training_data/" + "partys/" + fraction + "/" + account + "/"):
            file = open("../training_data/" + "partys/" + fraction + "/" + account + "/" + id, 'r')
            # tweets = np.append(tweets, [fraction, file.read()])
            tweetfraction.append(fraction)
            tweetcontent.append(file.read())

            file.close()

print("Finished reading")

from sklearn.feature_extraction.text import CountVectorizer

count = CountVectorizer()
data = np.asarray(tweetcontent)[1:5000]
features = count.fit_transform(data).toarray()
del data

labels = np.array([
    1,
    0,
    1,
    1
])


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
testdata = count.transform(["ich mag keine Autos", "ich mag Autos", "ich mag Himmel", "Anna mag keine Himmel",
                            "ich mag keine Himmel"]).toarray()
prediction = clf.predict(testdata)

print("Hello World")
