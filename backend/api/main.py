import os
import sys
import subprocess
import statistics
from twitter import *

api = Twitter(auth=OAuth(os.environ['ACCESS_TOKEN_KEY'], os.environ['ACCESS_TOKEN_SECRET'], os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET']))

def predict_party(twitter_handle):
    predictions = {}
    statuses = api.statuses.user_timeline(screen_name=twitter_handle, count=200)
    for status in statuses:
        prediction = subprocess.call(["python3", "../training/predict.py", str(status["text"])])
        prediction = json.loads(prediction.split("===JSON===")[-1])
        for key, value in prediction.items():
            if key not in predictions.keys():
                predictions[key] = []
            predictions[key].append(value)

    for key, value in predictions.items():
        predictions[key] = statistics.median(value)

    print(predictions)


if __name__ == '__main__':
    predict_party(sys.argv[1])
