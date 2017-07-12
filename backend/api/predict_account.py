import os
import sys
import subprocess
import statistics
import json

from twitter import *
import predict

with open("twitter.conf") as data_file:
	data = json.load(data_file)

api = Twitter(auth=OAuth(data['accessTokenKey'], data['accessTokenSecret'], data['consumerKey'], data['consumerSecret']))

def predict_party(twitter_handle):
    #logger_pdca.debug("Predicting " + twitter_handle)
    predictions = {}
    statuses = api.statuses.user_timeline(screen_name=twitter_handle, count=200)
    for status in statuses:
        prediction = predict.predict(status["text"])

        for key, value in prediction.items():
            if key not in predictions.keys():
                predictions[key] = []
            predictions[key].append(value)

    for key, value in predictions.items():
        # verbose: print(key, value)
        predictions[key] = statistics.mean(value)
    #logger_pdca.debug("=== done ====")
    return predictions


if __name__ == '__main__':
    print(json.dumps(predict_party(sys.argv[1])))
