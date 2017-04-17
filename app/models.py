from app import db


class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float)
    memo = db.Column(db.String(150))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    date = db.Column(db.Date)

    def __init__(self, amount, category, memo, date):
        self.amount = amount
        self.category = category
        self.memo = memo
        self.date = date

    def __repr__(self):
        return '<Transaction [{}/{}] {}:  {}>'.format(
            self.transaction_id,
            self.category,
            self.amount,
            self.date)


class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    category_rel = db.relationship('Transaction', backref='category', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category [{}] {}>'.format(
            self.category_id,
            self.name)