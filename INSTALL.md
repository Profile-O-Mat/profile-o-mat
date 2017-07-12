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
* github.com/gorilla/websocket
* github.com/ChimeraCoder/anaconda

# Getting things to run

## Generate API Keys and Acess Token:
Go to https://apps.twitter.com/, create an application, generate an access token and insert all the keys into `backend/twitter.conf` and `backend/api/twitter.conf`

## Set api key envvars
`$ source backend/twitter.conf`
`$ export ACCESS_KEY`
`$ export ACCESS_SECRET`
`$ export CONSUMER_KEY`
`$ export CONSUMER_SECRET`

## Get training data
First make sure there are no folders called `partys/` or `mdbs/` under `/training_data/` and execute `training_data/fetch_data.sh`. The script will fetch all members of the German parliament and their last 3200 tweets. The data will be stored in `partys/[party]/[twitter-handle]/[tweet-id].TXT`

## Train the network
After successfully receiving the training data you can navigate to `backend/train/` where you can execute `python train.py`. You can adjust `ITERATIONS` and `LAYER` inside the file. If the training process successfully finished, the data has been saved in `backend/train/export_*` using the python package pickle. An evaluation of the training process can be found in `train/evaluation.txt` aside the confusion matrix `train/confusion.jpg`.

### Already trained network
You can download an already trained network [here](https://www.dropbox.com/s/4pytchrk6axidtw/trained.zip?dl=0) ([Direct Download](https://www.dropbox.com/s/4pytchrk6axidtw/trained.zip?dl=1))

## Predict a single tweet
To predict a single tweet (or other pieces of text) use the python script `api/predict.py` with your piece of text as the first argument (e.g. `python predict.py "Hallo das ist ein text"`). Note again that the ANN is trained using tweets of German politicians and thus will not understand English words or text. The output will be JSON.

## Predict based on the last tweets of an account
Using the python script `predict_account.py [account name]` will request the last 200 tweets of the account holder, predict each one of them and eventually calculate the mean of all predictions. Again the ANN does not understand English, and the output is formatted in JSON.

## Run the backend
To host profile-o-mat on your server (contacting us before doing so would be appreciated) just copy the systemd unit files from `backend/systemd_units`. Please note that you may need to adjust the path specified in the documents.

To receive a prediction via HTTP execute a GET request on `localhost:5000/predict?user=twitter_handle`.

Please note that profile-o-mat is hosted with SSL using a Nginx reverse proxy so you may need to change the frontend ports.
