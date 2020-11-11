from flask import render_template, Flask
from flask_socketio import SocketIO

import classify

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
    lock_result = classify.should_lock(imagedata)

with open('unmasked.jpg', 'rb') as file:
    data = file.read()
    for i in range(0, 10):
        print(classify.should_lock(data))

with open('masked.jpg', 'rb') as file:
    data = file.read()
    for i in range(0, 10):
        print(classify.should_lock(data))

with open('unmasked.jpg', 'rb') as file:
    data = file.read()
    for i in range(0, 2):
        print(classify.should_unlock(data))

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    socketio.run(app, port='5000')

