# Flask-SocketIO Blueprint
----

A Blueprint class to be used with [Flask-SocketIO](http://flask-socketio.readthedocs.org/en/latest/)

### Install
```pip install git+http://github.com/m-housh/io-blueprint.git```  

### Simple Example
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
</html>
```
### Advanced Example
----

A more likely example as the above can easily be used without a blueprint type of pattern.  Such as in Miguel Grinberg's [Flask-SocketIO-Chat](https://github.com/miguelgrinberg/Flask-SocketIO-Chat).  

My use case is I have multiple sockets that provide similar functionality.  I have a single page app that all the content is loaded through a socket.  To keep things DRY I sub-class IOBlueprint with several methods that provide a form view, a table view and a way to process a form on submission.  It should also be noted that I use the [dominate](https://github.com/Knio/dominate) lib to create my views dynamically through code, and do not need to render html other than my initial view and/or login view (which is pre-socketio connection).

base.py
```python
from io_blueprint import IOBlueprint
from flask_socketio import emit

class Base(IOBlueprint):

    def __init__(self, namespace=None, **kwargs):
        self._form_view = kwargs.pop('form_view', None) # should return an html safe string to be loaded into the page
        self._table_view = kwargs.pop('table_view', None) # should return an html safe to be loaded into the page
        self.form = kwargs.pop('form', None) # should be a flask_wtf.Form class
        super().__init__(namespace, **kwargs)
        
        # events to be registered.
        @self.on('table')
        def table():
            emit('load content', str(self._table_view()), namespace='/')
    
        @self.on('form')
        def form():
            emit('load content', str(self._form_view(form=self.form())), namespace='/') # load a fresh form
            
        @self.on('post')
        def post(data):
            formdata = data.get('form')
            form = self.form(**formdata)
            if form.validate():
                # do something
                model = myDatabaseModel()
                form.populate_obj(model)
                # save model to database
                model.save()
                emit('flash', 'Model saved', namespace='/')
                # show the table view with new model
                emit('load content', str(self._table_view()), namespace='/')
                return # exit this method
            emit('flash', 'Please fix form errors', namespace='/')
            emit('load content', str(self._form_view(form=form)), namespace='/') # load the form with errors
            
    def _prepare_for_io(self):
        if self._table_view is None:
            raise ValueError('table_view not set on instance.')
        if self._form_view is None:
            raise ValueError('form_view not set on instance.')
        if self.form is None:
            raise ValueError('form not set on instance.')
        return True
        
    def init_io(self, io):
        self._prepare_for_io()
        return super().init_io(io)
```            
   
