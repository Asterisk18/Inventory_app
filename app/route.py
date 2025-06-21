from app import app, db, bcrypt
from flask import render_template , url_for , redirect , flash
from app.forms import RegistrationForm , LoginForm , ItemForm
from app.models import User , Item
from flask_login import login_user, logout_user, login_required, current_user
from app.decorators import admin_required


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register" , methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data , email=form.email.data , password = hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash("You account has been successfully Created", 'success')
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful!", "success")
            return redirect(url_for('home')) 
        else:
            flash(f"Login Unsuccesful, Please check the email and Password" , "danger")
    return render_template("login.html" , form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out" , "info")
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template("account.html")


@app.route("/update" , methods=['GET' , 'POST'])
@admin_required
def manage_inventory():

    form = ItemForm()
    if form.validate_on_submit():
        item = Item.query.filter_by(name = form.name.data).first()
        if item:
            item.quantity = form.quantity.data
            db.session.commit()
        else:
            new_item = Item(name = form.name.data , quantity = form.quantity.data)
            db.session.add(new_item)
            db.session.commit()
        flash("Item Updated" , "success")
        return redirect(url_for("manage_inventory"))
    items = Item.query.all()
    return render_template('manage_inventory.html' , form=form , items=items)

@app.route("/inventory")
def inventory():
    items = Item.query.order_by(Item.name).all()
    return render_template('inventory.html' , items = items)