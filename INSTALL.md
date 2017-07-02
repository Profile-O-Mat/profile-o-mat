# Dependencies
* python3.4+
* go

## Python packages:
* python-twitter
* requests
* numpy
* scipy
* scikit-learn

## go packages
* github.com/dghubble/go-twitter/twitter
* github.com/dghubble/oauth1
* github.com/dghubble/go-twitter/twitter
* github.com/dghubble/oauth1
* github.com/gorilla/websocket

## Generate Api Keys and Acess Token:
Go to https://apps.twitter.com/, create an application, generate an access token and insert all the keys into `backend/twitter_keys.sh`

# Running
By default, there is an already trained network included in the repo, so you don't have to train it yourself and can skip to `Predict a single tweet`

## Set api key envvars
`$ source backend/twitter_keys.sh`

## Get training data
in `backend/training_data` run `fetch_data.sh`. You should get a total of about 30 000 tweets, otherwise, something went wrong.

## Train the network
in `backend/training` run `python train.py`. You can adjust `ITERATIONS` and `LAYER` in this file.

## Predict a single tweet
run `python backend/api/predict.py "Text here"`

## Predict based on the last tweets of an acount
run `python backend/api/predict_account.py accountname`

## Run the backend
Go stuff, don't ask me

## Run the flask backend
install python package `flask`

run `python backend/api/main.py`

GET request to `localhost:5000/predict?user=twitter_handle`, get back json
