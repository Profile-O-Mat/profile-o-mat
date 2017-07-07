VECTOR_SIZE = 300

def vectorizeWord( word ):
	print("Searching for " + word)
	vector = [0] * VECTOR_SIZE # default empty vector
	with open("fasttext.vec", "r") as dataset:
		for row in dataset:
			cells = row.split(" ")
			if cells[0].lower() == word.lower():
				vector = cells[1:-1] # remove word, \n
				
				print("FOUND " + str(len(vector)) + " long vec.")
				break;
	print(vector)
	return

def vectorizeText( text ):
	vector = [0] * VECTOR_SIZE
	words = text.split(" ")
	length = len(words)
	print("Vectorizing [" + str(length) + "] " + text)
	for word in words:
		wordvec = vectorizeWord(word)
		for i in range(0, VECTOR_SIZE+1):
			print("Math for element " + str(i))
			vector[i] += wordvec[i] / length
	return vector

vectorizeText("Alpaca Hallo")
