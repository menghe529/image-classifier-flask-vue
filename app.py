import os
import sys
import json
from random import *
from flask_cors import CORS
from flask_restful import Resource, Api


# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
# from tensorflow.keras.models.load_weights import load_weights
from tensorflow.keras.preprocessing import image

# Some utilites
import numpy as np
from util import base64_to_pil

import datetime


# Declare a flask app
# app = Flask(__name__)
app = Flask(
    __name__,
    static_folder = "./dist/static",
    template_folder = "./dist"
)
api = Api(app=app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# clear cache
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = datetime.timedelta(seconds=1)


# You can use pretrained model from Keras
# Check https://keras.io/applications/
# or https://www.tensorflow.org/api_docs/python/tf/keras/applications

from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
model = MobileNetV2(weights='imagenet')

print('Model loaded. Check http://127.0.0.1:5000/')


# Model saved with Keras model.save()
MODEL_PATH = 'models/inception_v3_weights_tf_dim_ordering_tf_kernels.h5'

# Load your own trained model
# model = load_model(MODEL_PATH)
# model._make_predict_function()          # Necessary
# print('Model loaded. Start serving...')
model = tf.keras.models.load_model(MODEL_PATH, compile=False)


def model_predict(img, model):
    img = img.resize((224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='tf')

    preds = model.predict(x)
    return preds


# @app.route('/', methods=['GET'])
# def index():
#     # Main page
#     return render_template('index.html')
@app.route('/', methods=['GET'])
def index():
    #Main page
    return render_template("index.html")

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return render_template("index.html")


class Prediction(Resource):
    def post(self):    
        # print("Hello, world!")
        # app.logger.debug('A value for debugging')
        # Get the image from post request
        img = base64_to_pil(request.json)

        # Save the image to ./uploads
        img.save("./uploads/image.png")

        # Make prediction
        preds = model_predict(img, model)

        # Process your result for human
        # pred_proba = "{:.3f}".format(np.amax(preds))    # Max probability
        # print("-------pred_proda-------")
        # print(pred_proba)

        # pred_class = decode_predictions(preds, top=1)   # ImageNet Decode

        # test = decode_predictions(preds, top=5)[0]
        # print(test)
        # result = str(pred_class[0][0][1])               # Convert to string
        # result = result.replace('_', ' ').capitalize()
        pred_class = decode_predictions(preds, top=5)[0]

        result = []
        for val in pred_class:
            obj = {}
            obj[val[1]] = "{:.3f}".format(val[2])
            result.append(obj)
        print("-----result-----")
        print(json.dumps(result, ensure_ascii=False))
        # Serialize the result, you can add additional fields
        return jsonify(result=result)
api.add_resource(Prediction, '/api/prediction')


class RandomNumber(Resource):
    def get(self):
        response = {
            'randomNumber': randint(1, 100)
        }
        return response
api.add_resource(RandomNumber, '/api/random')
# @app.route('/api/random')
# def random_number():
#     response = {
#         'randomNumber': randint(1, 100)
#     }
#     return jsonify(response)

if __name__ == '__main__':
    # app.run(port=5002, threaded=False)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
