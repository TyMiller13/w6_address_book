from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, AddressForm, LoginForm
from app.models import User, Address


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contacts')
@login_required
def contacts():
    address = Address.query.all()
    return render_template('contacts.html', address=address)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    # create an instance of the SignUpForm
    form = SignUpForm()
    # Check if a POST request AND data is valid
    if form.validate_on_submit():
        # Get the data from the form
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        # Query our user table to see if there are any users with either username or email from form
        check_user = User.query.filter(
            (User.username == username) | (User.email == email)).all()
        # If the query comes back with any results
        if check_user:
            # Flash message saying that a user with email/username already exists
            flash('A user with that email and/or username already exists.', 'danger')
            return redirect(url_for('signup'))
        # If check_user is empty, creater a new record in the user table
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password)
        # Flash a success message
        flash(f'Thank you {first_name} {last_name} for signing up!', 'success')
        # redirect back to home
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

# create a route for address inputs to be stored in db model


@app.route('/address', methods=["GET", "POST"])
@login_required
def address():
    form = AddressForm()

    if form.validate_on_submit():
        # get data from form
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        print(first_name, last_name, phone_number, address)

        check_phone_number = Address.query.filter(
            (Address.phone_number == phone_number)).all()

        if check_phone_number:
            flash('A contact with that phone number already exists.', 'danger')
            return redirect(url_for('address'))

        new_address = Address(first_name=first_name, last_name=last_name,
                              phone_number=phone_number, address=address)
        flash(
            f"Your new contact info for {first_name} {last_name} has been added!", "success")
        return redirect(url_for('address'))
    return render_template('add_address.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # get the username and password from form
        username = form.username.data
        password = form.password.data
        print(username, password)
        # Query the user table to check if there is a user with that username
        user = User.query.filter_by(username=username).first()
        # Check if there is a user and that the password is correct
        if user is not None and user.check_password(password):
            # log the user in
            login_user(user)
            flash(f"{user.username} is now logged in", "warning")
            return redirect(url_for('index'))
        else:
            flash(f"Incorrect username and/or password", "danger")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(f"You have been logged out", "warning")
    return redirect(url_for('index'))


@app.route('/contacts/<int:address_id>', methods=["GET", "POST"])
@login_required
def get_info(address_id):
    info = Address.query.get(address_id)
    if not info:
        flash(f"A contact with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    return render_template('contact_info.html', info=info)


@app.route('/contacts/<int:address_id>/update', methods=["GET", "POST"])
@login_required
def update_contact(address_id):
    info = Address.query.get(address_id)
    if not info:
        flash(f"A contact with id# {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    form = AddressForm()
    if form.validate_on_submit():
        # get the form data
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        info.update(first_name=first_name, last_name=last_name,
                    phone_number=phone_number, address=address)
        flash(f"{info.first_name} {info.last_name} has been updated!", "success")
        # not redirecting to correct spot
        return redirect(url_for('get_info', address_id=address_id))
    if request.method == 'GET':
        form.first_name.data = info.first_name
        form.last_name.data = info.last_name
        form.phone_number.data = info.phone_number
        form.address.data = info.address
    return render_template('update_contact.html', info=info, form=form)


@app.route('/contacts/<address_id>/delete')
@login_required
def delete_post(address_id):
    contact = Address.query.get(address_id)
    if not contact:
        flash(f"A post with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    contact.delete()
    flash(f"{contact.first_name} {contact.last_name} has been deleted", "info")
    return redirect(url_for('index'))