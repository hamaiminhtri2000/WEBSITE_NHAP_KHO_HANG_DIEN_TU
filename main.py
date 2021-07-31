from flask import Flask, render_template, redirect, request
from flask.globals import session
from flask.helpers import flash
from forms import SignUpForm, SignInForm, AddProductForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HMMTri Python-Flask Web App'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models

@app.route('/')
def main():
    todolist = [
        {
            'ten': '',
            'noidung': ''
        }

    ]
    return render_template('index.html', todolist = todolist)

@app.route('/dangKy', methods=['GET', 'POST'])
def dangKy():
    form = SignUpForm()
    if form.validate_on_submit():
        print("Xác nhận khi gửi")
        _fname = form.inputFirstName.data
        _lname = form.inputLastName.data
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        #user = {'fname': _fname, 'lname': _lname, 'email': _email, 'password': _password}
        if (db.session.query(models.User).filter_by(email=_email).count() == 0):
            user = models.User(first_name=_fname, last_name=_lname, email=_email)
            user.set_password(_password)
            db.session.add(user)
            db.session.commit()
            return render_template('dangKySuccess.html', user=user)
        else:
            flash('Email {} đã tồn tại!'.format(_email))
            return render_template('dangky.html', form=form)

    print("Không xác nhận khi gửi")
    return render_template('dangky.html', form = form)

@app.route('/dangNhap', methods=['GET', 'POST'])
def dangNhap():
    form = SignInForm()

    if form.validate_on_submit():
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        user = db.session.query(models.User).filter_by(email=_email).first()
        if (user is None):
            flash('Sai Địa chỉ Email hoặc Mật Khẩu!')
        else:
            if (user.check_password(_password)):
                session['user'] = user.user_id
                #return render_template('tcnguoidung.html')
                flash('đăng nhập thành công!')
                return redirect('/productHome')
            else:
                flash('Sai Địa chỉ Email hoặc Mật Khẩu!')
    return render_template('dangnhap.html', form=form)

@app.route('/logOut')
def logout():
    session.pop('user', None)
    return redirect('/dangNhap')

@app.route('/productHome', methods=['GET', 'POST'])
def Product_Home():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        product = db.session.query(models.Product).all()
        approve = db.session.query(models.Approve).all()
        #Approve_Product = db.session.query(models.Product).filter_by(user_id=_user_id, approve=0).all()
        return render_template('home-product.html', user=user, product=product, approve=approve)
    else:
        return redirect('/dangNhap')


@app.route('/addProduct', methods=['GET', 'POST'])
def Add_product():
    form = AddProductForm()
    _user_id = session.get('user')

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        if form.validate_on_submit():
            _name = form.inputProductName.data
            _category = form.inputCategory.data
            _price = form.inputPrice.data
            _date = form.inputDate.data

            _product_id = request.form['hiddenProductId']
            if (_product_id == "0"):
                product = models.Product(product_name=_name, category=_category, price=_price, date=_date, approve_id = "1", user=user)
                db.session.add(product)
            else:
                product = db.session.query(models.Product).filter_by(product_id=_product_id).first()
                product.product_name = _name
                product.category = _category
                product.price = _price
                product.date = _date
            db.session.commit()
            return redirect('/productHome')

        return render_template('add-product.html', form=form, user=user)

    return redirect('/dangNhap')

@app.route('/approveProduct', methods=['GET', 'POST'])
def Approve_Product():
    _user_id = session.get('user')
    if _user_id:
        _product_id = request.form['hiddenApproveId']
        if _product_id:
            product = db.session.query(models.Product).filter_by(product_id=_product_id).first()
            product.approve_id = "2"
            db.session.commit()
        return redirect('/productHome')
    return redirect('/dangNhap')

@app.route('/editProduct', methods=['GET', 'POST'])
def Edit_Product():
    form = AddProductForm()
    _user_id = session.get('user')

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        product_id = request.form['hiddenProductId']
        if product_id:
            product = db.session.query(models.Product).filter_by(product_id=product_id).first()
            form.inputProductName.default = product.product_name
            form.inputCategory.default = product.category
            form.inputPrice.default = product.price
            form.inputDate.default = product.date
            form.process()

            return render_template('add-product.html', form=form, user=user, product=product)

    return redirect('/dangNhap')

@app.route('/removeProduct', methods=['GET', 'POST'])
def Remove_Product():
    _user_id = session.get('user')

    if _user_id:
        _product_id = request.form['hiddenProductId']
        if _product_id:
            product = db.session.query(models.Product).filter_by(product_id=_product_id).first()
            db.session.delete(product)
            db.session.commit()
        return redirect('/productHome')

    return redirect('/dangNhap')
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080', debug=True)