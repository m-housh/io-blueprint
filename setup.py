from setuptools import setup
version = '0.1.0'

setup(name='IOBlueprint',
        version=version,
        description='Adds Blueprint like functionality to Flask-Socketio',
        url='http://github.com/m-housh/io-blueprint.git',
        author='Michael Housh',
        author_email='mhoush@houshhomeenergy.com',
        packages=['io_blueprint'],
        install_requires=['flask_socketio']
)
