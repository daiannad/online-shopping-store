from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)
#DB-Table-Record
#Table
#id title price isActive
#1 Some 100 True
#2 Some2 200 False
#3 Some3 40 True
class Item(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    price=db.Column(db.Integer, nullable=False)
    isActive=db.Column(db.Boolean, default=True)
    #text=db.Column(db.text, nullable=False)
    def __repr__(self):
        return f'DATA: {self.title}'

@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/buy/<int:id>')
def item_buy(id):
    item=Item.query.get(id)
    api=Api(merchant_id=1396424,
            secret_key='test')
    checkout=Checkout(api=api)
    data={
        "currency":"GEL",
        "amount": item.price
    }
    url=checkout.url(data).get('checkout_url')
    return redirect(url)
def about():
    return render_template('about.html')
@app.route('/create')
def create():
    return render_template('create.html')
@app.route('/create', methods=['POST','GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        url = request.form['image']
        item=Item(title=title, price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "ERROR"
    else:
        return render_template('create.html')
if __name__=="__main__":
   app.run(debug=True)
