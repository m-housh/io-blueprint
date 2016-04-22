from io_blueprint import IOBlueprint
from bootstrap_wrapper import Div 
from flask_socketio import emit, SocketIO

io = SocketIO()


def flash(msg, category='info'):
    view = Div(msg,
        _class='alert alert-{}'.format(category))

    io.emit('flash', str(view), namespace='/')

@io.on('connect', namespace='/')
def connect():
    flash('You are connected. Please click a button.', 'success')

class BaseBlueprint(IOBlueprint):

    def __init__(self, namespace=None, **kwargs):
        self._table_view = kwargs.pop('table_view', None) # table_view renders a table
        # form_view renders a form for this instances form
        self._form_view = kwargs.pop('form_view', None)
        # form should be a flask_wtf.Form class
        self.form = kwargs.pop('form', None)
        self.model = kwargs.pop('model', None)
        super().__init__(namespace, **kwargs)

        @self.on('table')
        def table():
            emit('load content', str(self._table_view()), namespace='/')

        @self.on('form')
        def form():
            form = self.form()
            emit('load content', str(self._form_view(form)), namespace='/')

        @self.on('post')
        def post(data):
            formdata = data.get('form')
            form = self.form(**formdata)
            if not form.validate():
                flash('Please fix form errors', 'danger')
                emit('load content', str(self._form_view(form)), namespace='/')
            else:
                model = self.model(**formdata)
                model.save()
                flash('Succesfully saved model', 'success')
                emit('load content', str(self._table_view()), namespace='/')

            

    def table_view(self, f):
        """ A decorator to add a table_view. """
        if not callable(f):
            raise TypeError('table_view must wrap a callable')
        self._table_view = f

    def form_view(self, f):
        """ A decorator to add a form_view """
        if not callable(f):
            raise TypeError('form_view must wrap a callable')
        self._form_view = f

    def _prepare_for_io(self):
        # raise runtime errors if instance of blueprint is not set up correctly
        if self._table_view is None:
            raise ValueError('no table_view set on instance.')
        if self._form_view is None:
            raise ValueError('no form_view set on instance.')
        if self.form is None:
            raise ValueError('no form set on instance.')
        if self.model is None:
            raise ValueError('no model set on instance.')
        return True

    def init_io(self, io):
        if self._prepare_for_io():
            return super().init_io(io)
