from app import app, db
from time import strftime
import datetime
from .models import Transaction, Category
from flask import g, render_template, flash, redirect, request
from .forms import LoginForm, TransactionForm, CategoryForm, UploadForm
from sqlalchemy import desc, exists
from .logic import add_transcation, import_transaction, add_category


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
    uploadform = UploadForm()
    #flash(form.category.choices)
    #flash(form.errors)
    added = False
    uploaded = False
    if form.submit.data and form.validate():
        add_transcation(form)
        added=True
    elif uploadform.validate_on_submit():
        import_transaction(uploadform)
        uploaded=True
    return render_template('add.html', form=form, uploadform=uploadform, date=datetime.date.today().strftime("%Y-%m-%d"), added=added, uploaded=uploaded)


@app.route("/addcategory", methods=['GET', 'POST'])
def add_category():
    form = CategoryForm(request.form)
    added = False
    if request.method == 'POST':
        if add_category(form):
            added=True
    return render_template('addcategory.html', form=form, added=added)


@app.route("/stats")
def stats():
    return render_template('stats.html')


@app.route("/history")
def history():
    transactions = Transaction.query.order_by(desc('date'))
    return render_template('history.html', transactions=transactions)