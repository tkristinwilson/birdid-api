import io
from _io import BytesIO
import json
from PIL import Image
from pathlib import Path

from torchvision import models
import torchvision.transforms as transforms
from flask import Flask, jsonify, request
import torch
from fastai.vision.data import ImageDataBunch
from fastai.vision.learner import cnn_learner
from fastai.vision.transform import get_transforms
from fastai.vision.image import open_image
from fastai.vision import imagenet_stats
from fastai.basic_train import load_learner

app = Flask(__name__)

learner = load_learner('.','export.pkl')
learner.model.eval()

# takes image data in bytes, applies the series of transforms and returns a tensor.
def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)
  
def get_prediction(bytes):
    img = open_image(BytesIO(bytes))
    pred =  learner.predict(img)   
    return pred

@app.route('/hc')
def hello():
    return 'OK'

@app.route('/predict', methods=['POST'])
def predict():  
    if request.method == 'POST':     
        file = request.files['file']
        img_bytes = file.read()
        pred = get_prediction(img_bytes)
        probs = pred[2]
        return jsonify({
        "predictions": sorted(
            zip(learner.data.classes, map(float, probs)),
            key=lambda p: p[1],
            reverse=True
            )
        })        

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")