from flask import Flask
import requests
import time
import os
from waitress import serve

app = Flask(__name__)

last_time = time.time()


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/feed')
def feed():
    full_period = 3600  # seconds
    global last_time
    # IFTTT web hook.
    url = "https://maker.ifttt.com/trigger/feed_my_fish/with/key/cyxCoFl4NSAHCAZ1ZPW_jV"
    ifttt_key = os.environ['IFTTT_KEY']
    payload = ""
    headers = {'apikey': ifttt_key}

    ts = time.time()
    period = ts - last_time
    print(period)
    if period > full_period:
        response = requests.request("GET", url, data=payload, headers=headers)
        print(response.text)
        last_time = ts
        return {'message': 'Got it! Please wait about 15 minutes for IFTTT feeder response'}
    else:
        return {'message': 'My fish is full!, please wait for hours'}


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
