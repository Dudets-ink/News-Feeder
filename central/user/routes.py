from central.user import bp
from central.user.forms import LoginForm, RegisterForm, ResetPassswordRequestForm, \
    ResetPasswordForm
from central.models import User 
from central import db, login
from central.email import send_password_reset_email

from flask import redirect, url_for, render_template, flash, request, abort
from flask_login import login_user, current_user, login_required, logout_user


@bp.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.is_unic(form.username.data, form.email.data):
            user = User(
                username = form.username.data,
                email = form.email.data
            )
            user.set_password(form.password.data)
            flash('You successfully pass registration!', 'success')
            # add remember me feature
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        
        flash('Please check your information', 'error')
        return redirect(url_for('user.register'))
    return render_template('user/register.html', form=form, title='Registration')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username_email.data).first()
        email = User.query.filter_by(email=form.username_email.data).first()
        if username or email:
            login_user(username or email)
            flash('You successfully log in!', 'success')
            return redirect(url_for('main.index'))
    return render_template('user/login.html', form=form, title='Login')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You successfully logged out!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user/profile.html', user=user)
    
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPassswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check you email for the instructions to reset your password')
            return redirect(url_for('main.index'))
    return render_template('user/password_reset_request.html',
                               title='Reset password', form=form)
        
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authienticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('main.index'))
    return render_template('user/reset_password.html', form=form)

@bp.route('/up_rank/<username>', methods=['GET', 'POST'])
def up_rank(username):
    user = User.query.filter_by(username=username).first()
    user.reputation += 1
    db.session.commit()
    url = request.args.get('next')
    return redirect(url)

@bp.route('/down_rank/<username>')
def down_rank(username):
    print('\nn\n\n\\n\n\n\n\n\n\n\n', username)
    user = User.query.filter_by(username=username).first()
    user.reputation -= 1
    db.session.commit()
    url = request.args.get('next')
    print('\nn\n\n\n\n\n\n\n\\n\n\n\n\n\n', url)
    return redirect(url)