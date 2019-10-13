#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, Response
import requests
import hashlib
import time
apiKey = "1m6lfng9fqd5fkv57r1c0cms70"
secret = "60mdjb6pisd5u"
timestamp = str(int(time.time()))
authHeaderValue = "EAN APIKey=" + apiKey + ",Signature=" + hashlib.sha512(apiKey+secret+timestamp).hexdigest() + ",timestamp=" + timestamp
base_url = 'https://api.ean.com/2.1/'


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/location', methods=['GET', 'POST'])
def worker():
    # data = request.get_json()
    # result = 'hello world'
    # return result
    params = {
        "retina_name": "en_associative",
        "start_index": 0,
        "max_results": 1,
        "sparsity": 1.0,
        "get_fingerprint": False
    }
    requests.get(url=base_url + 'properties/22135/')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=80)