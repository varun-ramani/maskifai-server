from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import model
import json, time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('image')
def handle_message(message):
    print("received", time.time())
    data = json.dumps(model.test(message))
    print("sending", data, time.time())
    emit('faces', data)

if __name__ == '__main__':
    socketio.run(app)
    
