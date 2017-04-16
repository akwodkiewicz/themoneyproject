from app import app, db
from time import strftime
import datetime
from .models import Transaction, Category
from flask import g, render_template, flash, redirect, request
from .forms import LoginForm, TransactionForm, CategoryForm
from sqlalchemy import desc, exists

#q = Category.query.all()
#categories = list(set([(row.name, row.name) for row in q]))

@app.route("/")
@app.route("/index")
def index():
    return render_template('home.html')
    
@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID={}, remeber_me={}'.format(
			form.openid.data, str(form.remember_me.data)))
		return redirect('/index')
	return render_template('login.html',
							form=form,
							providers=app.config['OPENID_PROVIDERS'])


@app.route("/add", methods=['GET', 'POST'])
def add():
	form = TransactionForm(request.form)
	form.category.choices = [(row.category_id, row.name) for row in Category.query.all()]
	#flash(form.category.choices)
	#flash(form.errors)
	if request.method == 'POST' and form.validate():
		amount = 0
		if form.outflow.data != 0:
			amount = (-1)*form.outflow.data
		elif form.inflow.data != 0:
			amount = form.inflow.data
		cat = Category.query.filter_by(category_id=form.category.data).first()
		transaction = Transaction(amount, cat, form.memo.data, form.date.data)
		db.session.add(transaction)
		db.session.commit()
		print(transaction)
		return render_template('add.html', form=form,  date=datetime.date.today().strftime("%Y-%m-%d"), added=True)
	return render_template('add.html', form=form, date=datetime.date.today().strftime("%Y-%m-%d"), added=False)


@app.route("/addcategory", methods=['GET', 'POST'])
def add_category():
	form = CategoryForm()
	added = False
	if request.method == 'POST':
		print(db.session.query(Category.category_id).filter_by(name=form.category.data).scalar())
		if db.session.query(Category.category_id).filter_by(name=form.category.data).scalar() is None:
			category = Category(form.category.data)
			db.session.add(category)
			db.session.commit()
			added=True
	return render_template('addcategory.html', form=form, added=added)


@app.route("/stats")
def stats():
	return render_template('stats.html')


@app.route("/history")
def history():
	transactions = Transaction.query.order_by(desc('date'))
	return render_template('history.html', transactions=transactions)