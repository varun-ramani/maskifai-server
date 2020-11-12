from flask import render_template, Flask
from flask_socketio import SocketIO

import classify
from classify import should_lock
import lockintegration

import cv2

from lockintegration import lock

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
    classifier_ready = classify.feed_image(imagedata)

    if classifier_ready:
        if lockintegration.locked:
            if classify.should_unlock():
                print("Unlocking")
                lockintegration.unlock()
        else:
            if classify.should_lock():
                print("Locking")
                lockintegration.lock()


webcam = cv2.VideoCapture(0)
while True:
    (rval, image) = webcam.read()

    cv2.imshow('LIVE',   image)
    handle_image(image)
    key = cv2.waitKey(10)
    # if Esc key is press then break out of the loop
    if key == 27:  # The Esc key
        break


webcam.release()
cv2.destroyAllWindows()


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    socketio.run(app, port='5000')
