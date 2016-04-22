import sys
from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired
from bootstrap_wrapper import QuickForm, Div, Table, TableHeader, TableRow, Button
from dominate.tags import script
from ..base import BaseBlueprint, flash

# mock database
users = [{'first_name': 'John', 'last_name': 'Doe'}, 
        {'first_name': 'Foo', 'last_name': 'Bar'} ]

class UserForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])

class UserModel:
    def __init__(self, first_name=None, last_name=None, **kwargs):
        self.first_name = first_name or kwargs.pop('first_name')
        self.last_name = last_name or kwargs.pop('last_name')

    def save(self):
        users.append({ 'first_name': self.first_name, 'last_name': self.last_name})

user = BaseBlueprint('/user', form=UserForm, model=UserModel)

@user.form_view
def form(form):
    return Div(QuickForm(form),
            Button('Submit',
                primary=True,
                onclick="submitUserForm()"),
            script(src='/static/submitUserForm.js',
                type='text/javascript'))

@user.table_view
def table():
    view = Table(TableHeader('First Name', 'Last Name'), bordered=True, striped=True)
    for user in users:
        view.add(TableRow(user['first_name'], user['last_name']))

    return view

    



