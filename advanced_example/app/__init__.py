from flask import Flask
from flask_socketio import SocketIO
from bootstrap_wrapper import BootstrapDocument, Div, Button
from dominate.tags import script, h1, h3
from .blueprints.user import user as user_io
from .base import io

def create_app(debug=False):

    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'secret'

    @app.route('/')
    def index():
        doc = BootstrapDocument()
        # add socket-io client to the doc and our custom js.
        doc.scripts.add(script(
            src='//cdn.socket.io/socket.io-1.4.5.js',
            type='text/javascript'),
            script(src='/static/my.js',
                type='text/javascript'))

        doc.body.children.insert(0, Div(h1('Advanced Example'), 
            Div(h3('Flashes'), Div(id='flashes')))) 
        
        # add buttons below the content of the document
        doc.body.add(Button(
            'Table',
            onclick="user_socket.emit('table');"),
            Button('Form',
                onclick="user_socket.emit('form');"))

        return doc.render()


    io.init_app(app)
    user_io.init_io(io)
    return app
