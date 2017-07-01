import os
import sys
import subprocess
import statistics
import json
from twitter import *

api = Twitter(auth=OAuth(os.environ['ACCESS_TOKEN_KEY'], os.environ['ACCESS_TOKEN_SECRET'], os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET']))

def predict_party(twitter_handle):
    predictions = {}
    statuses = api.statuses.user_timeline(screen_name=twitter_handle, count=10)
    for status in statuses:
        wd = os.getcwd()
        os.chdir("../training")
        j = str(subprocess.check_output(["python3", "./predict.py", str(status["text"])]))
        j = j.split("===JSON===")[-1][:-1]
        j = j.replace(r"\n", "")
        print(j)
        prediction = json.loads(j)
        os.chdir(wd)
        for key, value in prediction.items():
            if key not in predictions.keys():
                predictions[key] = []
            predictions[key].append(value)

    for key, value in predictions.items():
        print(key, value)
        predictions[key] = statistics.median(value)
    print("=== done ====")
    return predictions


if __name__ == '__main__':
    print(predict_party(sys.argv[1]))
