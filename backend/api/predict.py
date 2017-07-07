import sys
import pickle
import json

## Load logic
#logger_pdc.debug("Importing data structure: ")

clf = None
count = None
fractions = None

#logger_pdc.debug(" -> CountVectorizer")
with open("../training/export_count.dat", "rb") as handle:
	count = pickle.load(handle)

#logger_pdc.debug(" -> MLPClassifier")
with open("../training/export_clf.dat", "rb") as handle:
	clf = pickle.load(handle)

#logger_pdc.debug(" -> Fractions")
with open("../training/export_fractions.dat", "rb") as handle:
	fractions = pickle.load(handle)


def predict(tweet):
	## Predict
	features = count.transform({tweet}).toarray()
	prediction = clf.predict_proba(features)
	results = {}

	for key, value in fractions.items():
		for i in range(0, len(clf.classes_) - 1 + 1): #range is exclusive upper bound
			if clf.classes_[i] == value:
				results[key] = prediction[0][i]
	return results

if __name__ == '__main__':
	if (len(sys.argv) != 2):
		print('Illigal arguments!')
		exit()

	tweet = sys.argv[1]
	#logger_pdc.debug(tweet)
	#logger_pdc.debug("===JSON===")
	print(json.dumps(predict(tweet)))
