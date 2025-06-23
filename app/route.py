from datetime import datetime
from app import app, db, bcrypt
from flask import render_template , url_for , redirect , flash , request
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

@app.route("/inventory" , methods=['GET' , 'POST'])
def inventory():
    query = request.args.get('q', '').strip().lower()
    items = Item.query.order_by(Item.name).all()

    if query:
        items = [item for item in items if query in item.name.lower()]

    if request.method == 'POST' and current_user.is_authenticated and current_user.is_admin:
        item_id = request.form.get('item_id')
        action = request.form.get('action')
        item = Item.query.get(item_id)

        if item:
            if action == "add":
                item.quantity +=1
            elif action == "deduct" and item.quantity>0:
                item.quantity -=1
            elif action == "set":
                try:
                    quantity = int(request.form.get('quantity'))
                    if quantity>0:
                        item.quantity = quantity
                    else:
                        flash("The quantity cannot be negative" , "warning")
                except:
                    flash("Error occured in the process" , "danger")

                item.last_updated = datetime.utcnow()
                db.session.commit()
                    
            item.last_updated = datetime.utcnow()
            db.session.commit()
            flash("Item value Updated Succesfully" , "success")
        else:
            flash("Item not found" , "danger")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template("inventory_results.html", items=items)
    # items = Item.query.order_by(Item.name).all()
    return render_template('inventory.html' , items = items)


@app.route("/add_item" , methods=['GET' , 'POST'])
@login_required
@admin_required
def add_item():
    form = ItemForm()

    if form.validate_on_submit():
        item = Item(name = form.name.data , quantity = form.quantity.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('inventory'))
    return render_template('add_item.html' , form=form)

@app.route("/edit_item/<int:item_id>" , methods=['GET' , 'POST'])
@login_required
@admin_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = ItemForm(obj=item)
    form.original_name = item.name

    if form.validate_on_submit():
        item.name = form.name.data
        item.quantity = form.quantity.data
        item.last_updated = datetime.utcnow()
        db.session.commit()
        flash("Item details Updated" , "success")
        return redirect(url_for('inventory'))
    
    return render_template('edit_item.html' , form=form , item=item)
        
@app.route("/delete_item/<int:item_id>" , methods=['POST'])
@login_required
@admin_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

    flash("Item deleted Successfully" , "success")
    return redirect(url_for("inventory"))
