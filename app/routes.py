from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm
from app.models import User, Address


@app.route('/')
def index():
    return render_template('index.html')


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
        new_user = User(first_name=first_name, last_name=last_name,
                        email=email, username=username, password=password)
        # Flash a success message
        flash(f'Thank you {first_name} {last_name} for signing up!', 'success')
        # redirect back to home
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

# create a route for address inputs to be stored in db model
