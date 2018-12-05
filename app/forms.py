from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SubmitField
from wtforms.validators import Required

class SearchForm(Form):
    search = TextField('Type organism name:', validators = [Required()])
    submit_button = SubmitField('Search')