import os
import sys
import subprocess
import statistics
import json
from twitter import *

import importlib.util
spec = importlib.util.spec_from_file_location("predict", "../training/predict.py")
predict = importlib.util.module_from_spec(spec)
d = os.getcwd()
os.chdir("../training/")
spec.loader.exec_module(predict)
os.chdir(d)

api = Twitter(auth=OAuth(os.environ['ACCESS_TOKEN_KEY'], os.environ['ACCESS_TOKEN_SECRET'], os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET']))

def predict_party(twitter_handle):
    predictions = {}
    statuses = api.statuses.user_timeline(screen_name=twitter_handle, count=100)
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
