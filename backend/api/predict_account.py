import os
import sys
import subprocess
import statistics
import json
from twitter import *

import predict

api = Twitter(auth=OAuth(os.environ['ACCESS_TOKEN_KEY'], os.environ['ACCESS_TOKEN_SECRET'], os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET']))

def predict_party(twitter_handle):
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
    print("=== done ====")
    return predictions


if __name__ == '__main__':
    print(predict_party(sys.argv[1]))
