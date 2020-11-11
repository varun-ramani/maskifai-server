from flask import render_template, Flask
from flask_socketio import SocketIO

import classify
from classify import should_lock
import lockintegration

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

socketio = SocketIO(app)


@socketio.on('connect')
def connected():
    print('connected')


@socketio.on('disconnect')
def disconnected():
    print('disconnected')


@socketio.on('image')
def handle_image(imagedata):
    classifier_ready = classify.feed_image()
    if classifier_ready:
        if lockintegration.locked and classify.should_unlock():
            lockintegration.unlock()
        elif not lockintegration.locked and classify.should_unlock():
            lockintegration.lock()

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    socketio.run(app, port='5000')
