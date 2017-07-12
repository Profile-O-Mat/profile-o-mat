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
    try:
	    statuses = api.statuses.user_timeline(screen_name=twitter_handle, count=200)
    except TwitterHTTPError as error:
        if "error" in error.response_data:
            return dict({"success": False, "error": error.response_data["error"], "data": {}})
        if "errors" in error.response_data:
            return dict({"success": False, "error": error.response_data["errors"][0], "data": {}})
        return dict({"success": False, "error": "unknown", "data": {}})
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
    return dict({"success": True, "error": {}, "data": predictions})


if __name__ == '__main__': # Only happens if called manualy or by go backend
    result = predict_party(sys.argv[1])
    if (result["success"] == True):
        print(json.dumps(result["data"]))
        exit(0)
    print(json.dumps(result["error"])) # error message will appear in journal
    exit(1) # Go backend will quit and not relay error to user

