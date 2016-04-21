from flask import Flask, render_template
from flask_socketio import SocketIO
from blueprint import test_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

io = SocketIO(app)
test_blueprint.init_io(io)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    io.run(app, debug=True)




