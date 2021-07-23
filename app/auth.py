from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.__init__ import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__) # declaring blueprint

@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user: # if user exists
            if check_password_hash(user.password,password): # checking password
                flash('Logged in successfully', category='success')
                login_user(user, remember=False) # keeping the login while website is open
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('No user found with entered e-mail', category='error')
    
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required # only executes if user is logged in
def logout():
    logout_user()
    flash('Logged out', category='info')
    return redirect(url_for('views.index'))

@auth.route('/sign-up', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # checking for errors
        user = User.query.filter_by(email=email).first()
        if user:
            flash('E-mail already used', category='error')
        elif len(email) < 7:
            flash('E-mail must be at least 7 characters long', category='error')
        elif len(first_name) < 2:
            flash('First Name must be at least 2 characters long', category='error')
        elif len(last_name) < 2:
            flash('Last Name must be least 2 characters long', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters long', category='error')
        elif password1 != password2:
            flash('Make sure the passwords match', category='error')
        else: # create user
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False) # logging in after creating account
            flash('Account created successfully', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign-up.html', user=current_user)

@auth.route('/update', methods=['POST','GET'])
@login_required
def update():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user and email == current_user.email:
            if first_name: # if first name box was filled
                if len(first_name) < 2:
                    flash('First Name must be at least 2 characters long', category='error')
                else:
                    user.first_name = first_name
            if last_name: # if last name box was filled
                if len(last_name) < 2:
                    flash('Last Name must be least 2 characters long', category='error')
                else:
                    user.last_name = last_name
            if password1 and not password2: # only password 1 filled
                flash('Fill the box confirming the new password', category='error')
            if password2 and not password1: # only password 2 filled
                flash('Fill the box to create the new password', category='error')
            if password1 and password2: # if both password boxes ware filled
                if len(password1) < 8:
                    flash('Password must be at least 8 characters long', category='error')
                elif password1 != password2:
                    flash('Make sure the passwords match', category='error')
                else:
                    hash_pass = generate_password_hash(password1, method='sha256')
                    user.password = hash_pass
            # no boxes filled
            if not first_name and not last_name and not password1 and not password2:
                flash('No changes to your account', category='warning')
            else:
                db.session.commit()
                flash('Account information updated', category='info')
        else:
            flash('Incorrect e-mail', category='error')

    return render_template('update.html', user=current_user)
