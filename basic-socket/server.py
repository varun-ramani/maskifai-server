from flask import Flask, render_template
from flask_socketio import SocketIO

import model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('image')
def handle_message(message):
    if any(model.test(message)):
        socket.emit('antimasker')

if __name__ == '__main__':
    socketio.run(app)
    
