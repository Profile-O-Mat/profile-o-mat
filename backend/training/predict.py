import sys
import pickle
import json

if (len(sys.argv) != 2):
	print('Illigal arguments!')
	exit()

tweet = sys.argv[1]

## Load logic
print("Importing data structure: ")

clf = None
count = None
fractions = None

print(" -> CountVectorizer")
with open("export_count.dat", "rb") as handle:
	count = pickle.load(handle)

print(" -> MLPClassifier")
with open("export_clf.dat", "rb") as handle:
	clf = pickle.load(handle)

print(" -> Fractions")
with open("export_fractions.dat", "rb") as handle:
	fractions = pickle.load(handle)

print("===JSON===")

## Predict
features = count.transform({tweet}).toarray()
prediction = clf.predict_proba(features)

for key, value in fractions.items():
	for i in range(0, len(clf.classes_) - 1 + 1): #range is exclusive upper bound
		if clf.classes_[i] == value:
			fractions[key] = prediction[0][i]

print(json.dumps(fractions))
