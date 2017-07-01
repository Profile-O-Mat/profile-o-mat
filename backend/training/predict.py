import sys
import pickle

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

## Predict
features = count.transform({tweet}).toarray()
prediction = clf.predict_proba(features)

print(fractions)
print(clf.classes_)
print(prediction)

print("EOF!")
