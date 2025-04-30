from flask import Flask, render_template, request, redirect, url_for, flash,session

from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField,PasswordField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired, Email,Length



app = Flask(__name__,template_folder='Templates')

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost:3306/app_users'
app.config['SECRET_KEY']='my_secret_key_no_one_can_access'

db=SQLAlchemy(app)

class Farmer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(800),nullable=False)

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(800), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register_B', methods=['GET', 'POST'])
def register_B():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_buyer = Buyer.query.filter_by(name=form.name.data).first()

        if existing_buyer:
            flash("Username already exists! Try a different one.", "danger")
        else:
            hashed_password = generate_password_hash(form.password.data)
            new_buyer = Buyer(name=form.name.data, password=hashed_password)
            db.session.add(new_buyer)
            db.session.commit()
            flash("Buyer registered successfully! Please log in.", "success")
            return redirect(url_for('login_B'))

    return render_template('register_B.html', form=form)


@app.route('/register_S', methods=['GET', 'POST'])
def register_S():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_farmer = Farmer.query.filter_by(name=form.name.data).first()

        if existing_farmer:
            flash("Username already exists! Try a different one.", "danger")
        else:
            hashed_password = generate_password_hash(form.password.data)
            new_farmer = Farmer(name=form.name.data, password=hashed_password)
            db.session.add(new_farmer)
            db.session.commit()
            flash("Seller registered successfully! Please log in.", "success")
            return redirect(url_for('login_S'))

    return render_template('register_S.html', form=form)

@app.route('/login_S', methods=['POST','GET'])
def login_S():
    form = LoginForm()

    if form.validate_on_submit():
        farmer = Farmer.query.filter_by(name=form.name.data).first()

        if farmer and check_password_hash(farmer.password, form.password.data):
            session['farmer_id'] = farmer.id
            flash("Seller login successful!", "success")
            return redirect(url_for('Seller_page'))
        else:
            flash("Invalid Seller username or password", "danger")

    return render_template('login_S.html', form=form)


@app.route('/login_B', methods=['POST','GET'])
def login_B():
    form=LoginForm()

    if form.validate_on_submit():
        existing_user=Buyer.query.filter_by(name=form.name.data).first()
        if existing_user and check_password_hash(existing_user.password, form.password.data):
            session['buyer_id'] = existing_user.id
            flash("Login successful!", "success")
            return redirect(url_for('Buyer_page'))
        else:
            flash("Invalid username or password", "danger")

    return render_template('login_B.html',form=form)


@app.route('/Buyer')
def Buyer_page():
    return render_template('Buyer.html')

@app.route('/Seller')
def Seller_page():
    return render_template('Seller.html')

@app.route('/veges')
def veges():
    return render_template('veges.html')

@app.route('/grains_s')
def grains_s():
    return render_template('grains_s.html')

@app.route('/fruits_s')
def fruits_s():
    return render_template('fruits_s.html')

@app.route('/fruits.html')
def old_fruits():
    return redirect(url_for('fruits_s'))

@app.route('/grains.html')
def old_grains():
    return redirect(url_for('grains_s'))

@app.route('/vegetables.html')
def old_veges():
    return redirect(url_for('veges'))

@app.route('/fruits_b.html')
def fruits_b():
    return render_template('fruits_b.html')

@app.route('/veges_b.html')
def veges_b():
    return render_template('veges_b.html')

@app.route('/grains_b.html')
def grains_b():
    return render_template('grains_b.html')

@app.route('/sellingFRUITS.html')
def veges_potatos():
    return render_template('veges_potatos.html')

@app.route('/about_us.html')
def about_us():
    return render_template('veges_potatos.html')

@app.route('/contact_us.html')
def contact_us():
    return render_template('veges_potatos.html')



if __name__=='__main__':
    app.run(debug=True)