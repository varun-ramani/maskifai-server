from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('image')
def handle_message(message):
    open("message", "wb").write(message)

if __name__ == '__main__':
    socketio.run(app)
    
