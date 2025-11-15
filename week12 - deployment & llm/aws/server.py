#!/usr/bin/env python
# coding: utf-8

import joblib
from flask import Flask
from flask import jsonify, request
from flask_cors import CORS
from waitress import serve

def load_model_file(filename):
    pipeline = joblib.load(filename)
    return pipeline

def predict(model, sentences):
    sentences = sentences if isinstance(sentences, list) else [sentences]
    pred = model.predict(sentences)

    return ['positive' if x == 1 else 'negative' for x in pred]

model = load_model_file('movie_model.pkl')

print('tests')
print(predict(model, 'this is a great movie.'))
print(predict(model, 'this is a horrible movie.'))
print('-'*60)

app = Flask(__name__)
CORS(app)

@app.route('/')
def start():
    sentence = request.args.get('sentence')
    
    if sentence == None: 
        return jsonify({})

    print('sentence:', sentence)
    
    result = predict(model, sentence)
    
    # print(result)
    return jsonify({
        'sentence': sentence,
        'sentiment': result[0]
    })

if __name__ == '__main__':
    print('server starting')
    serve(app, host="0.0.0.0", port=80)





