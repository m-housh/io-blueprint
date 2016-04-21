# Flask-SocketIO Blueprint
----

A Blueprint class to be used with [Flask-SocketIO](http://flask-socketio.readthedocs.org/en/latest/)

### Install
```pip install git+http://github.com/m-housh/io-blueprint.git```  

### Example
```
git clone http://github.com/m-housh/io-blueprint.git
cd io-blueprint/example
mkvirtualenv --python=$(which python3) io-blueprint
pip install -r requirements.txt
python app.py
```
----

app.py
```python
from flask import Flask, render_template
from flask_socketio import SocketIO
from blueprint import test_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route('/')
def index():
    return render_template('index.html')

io = SocketIO(app)
test_blueprint.init_io(io)

if __name__ == '__main__':
    io.run(app, debug=True)
```

blueprint.py
```python
from io_blueprint import IOBlueprint
from flask_socketio import emit

test_blueprint = IOBlueprint('/test')

@test_blueprint.on('say')
def say():
    emit('flash', "Server says...", namespace='/')
    
@test_blueprint.on('echo')
def echo(msg):
    emit('flash', msg.get('data'), namespace='/')
```

static/my.js
```javascript
var global_socket;
var test_socket;

$(document).ready(function(){
    namespace = '/'
    global_socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    test_socket = io('/test');
    
    global_socket.on('flash', function(msg){
        $('flashes').append('<br>' + $('<div/>').text(msg).html());
    });
    
    $('form#echo').submit(function(event){
        test_socket.emit('echo', {data: $('#message').val()});
        return false;
    });
})
```

templates/index.html
```html
<!DOCTYPE html>
<html>
    <head>
        <title>IOBlueprint Example</title>
    </head>
    <body>
        <div>
            <button onclick="test_socket.emit('say');" type="button">Say</button>
        </div>
        <div>
            <form name="echo" id="echo">
                <label for="message">Echo This</label>
                <br>
                <input type="text" name="message" id="message>
                <br>
                <input type="submit" value="Echo">
            </form>
        </div>
        <div id="flashes">
            <h3>Flash Messages</h3>
        </div>
        <div id="scripts">
            <script src="//ajax.googlapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
            <script src="//cdn.socket.io/socket.io-1.4.5.js" type="text/javascript"></script>
            <script src="/static/my.js" type="text/javascript"></script>
        </div>
    </body>
</html
```
