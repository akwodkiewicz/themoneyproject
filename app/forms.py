from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, DecimalField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
	openid = TextField('openid', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class TransactionForm(FlaskForm):
	outflow = DecimalField('Outflow', validators=[NumberRange(min=0)])
	inflow = DecimalField('Inflow', validators=[NumberRange(min=0)])
	memo = TextField('Memo', validators=[DataRequired()])
	category = SelectField('Category', coerce=int)
	date = DateField('Date')
	submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
	category = TextField('Category', validators=[DataRequired])
	submit = SubmitField('Submit')