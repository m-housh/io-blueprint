from io_blueprint import IOBlueprint
from flask_socketio import emit

test_blueprint = IOBlueprint('/test')

@test_blueprint.on('say')
def say():
    emit('flash', "I'm saying something", namespace='/')

@test_blueprint.on('echo')
def echo(msg):
    emit('flash', msg.get('data'), namespace='/')

