from flask import Flask, request, jsonify
from predict_account import predict_party

app = Flask(__name__)

@app.route('/predict')
def predict():
    twitter_handle = request.args.get('user')
    return jsonify(predict_party(twitter_handle))


if __name__ == '__main__':
    app.run()
