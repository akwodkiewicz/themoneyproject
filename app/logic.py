import os, csv
from datetime import datetime
from app import db
from .forms import LoginForm, TransactionForm, CategoryForm, UploadForm
from .models import Transaction, Category
from sqlalchemy import desc, exists
from .convert import csv_convert
from werkzeug import secure_filename


def add_transcation(form):
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

def import_transaction(form):
    filename = 'uploads/'+secure_filename(form.file.data.filename)
    form.file.data.save(filename)
    newfilename = csv_convert(filename)
    os.remove(filename)
    with open(newfilename, 'r') as f_in:
        reader = csv.reader(f_in, delimiter=',')
        counter = 0
        for line in reader:
            try:
                date = datetime.strptime(line[0], '%Y-%m-%d')
                category_name = line[1]
                memo = line[2]
                amount = line[3]
                print(Category.query.filter_by(name=category_name).first())
                category = Category.query.filter_by(name=category_name).first()
                if category is None:
                    category = Category.query.filter_by(name='Undefined').first()
                transaction = Transaction(amount, category, memo, date)
                db.session.add(transaction)
                counter +=1
            except ValueError as err:
                print(err)
            except IndexError:
                pass
        db.session.commit()
        print("Inserted {} transactions!".format(counter))
    os.remove(newfilename)

def add_category(form):
    print(db.session.query(Category.category_id).filter_by(name=form.category.data).scalar())
    if db.session.query(Category.category_id).filter_by(name=form.category.data).scalar() is None:
        category = Category(form.category.data)
        db.session.add(category)
        db.session.commit()
        return True
    return False