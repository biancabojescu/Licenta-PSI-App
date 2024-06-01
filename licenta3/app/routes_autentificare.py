from flask import render_template, redirect, url_for, session, flash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

from app import app, db, mail
from app.forms import LoginForm, RegistrationForm
from app.models import User, Institutie
from werkzeug.security import generate_password_hash, check_password_hash


# register
def send_email(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender=app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)


@app.route('/register', methods=['GET'])
def register():
    institutii = Institutie.query.all()
    hospital_choices = [(institutie.nume, institutie.nume) for institutie in institutii]

    form = RegistrationForm()
    form.hospital.choices = hospital_choices

    return render_template('register.html', title='Register', form=form)


@app.route('/register_user', methods=['POST'])
def register_user():
    form = RegistrationForm()
    institutii = Institutie.query.all()
    hospital_choices = [(institutie.nume, institutie.nume) for institutie in institutii]
    form.hospital.choices = hospital_choices

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        institutie = Institutie.query.filter_by(nume=form.hospital.data).first()

        if not institutie:
            flash('Selected hospital does not exist. Please choose a valid hospital.', 'error')
            return redirect(url_for('register'))

        user = User(
            nume=form.last_name.data,
            prenume=form.first_name.data,
            email=form.email.data,
            profesie=form.profession.data,
            parola=hashed_password,
            is_auth=False,
            role='user',
            id_institutie=institutie.id,
            email_confirmed=False
        )
        db.session.add(user)
        db.session.commit()

        token = user.get_reset_password_token()
        subject = "Please confirm your email"
        html = render_template('email_confirmation.html', user=user, token=token)
        send_email(user.email, subject, html)

        session['show_success_message'] = True
        flash('Congratulations, registration successful! Please check your email to confirm your registration.', 'success')
        return redirect(url_for('register'))
    else:
        session['show_error_message'] = True
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f"{fieldName}: {err}", 'error')
    return render_template('register.html', title='Register', form=form)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=str(app.config['SECURITY_PASSWORD_SALT']))


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=str(app.config['SECURITY_PASSWORD_SALT']), max_age=expiration)
    except:
        return False
    return email


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('index'))

    user = User.query.filter_by(email=email).first_or_404()

    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.email_confirmed = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('login'))


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if not user.email_confirmed:
                flash('Please confirm your email first.', 'warning')
                return redirect(url_for('login'))
            session['is_authenticated'] = True
            session['role'] = user.role
            session['profesie'] = user.profesie
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html', title='Login', form=form)


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.parola, form.password.data):
            if not user.email_confirmed:
                flash('Please confirm your email first.', 'warning')
                return redirect(url_for('login'))
            user.is_auth = True
            db.session.commit()
            session['is_authenticated'] = True
            session['user_id'] = user.id
            session['role'] = user.role
            session['profesie'] = user.profesie
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', title='Login', form=form)


# logout
@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            user.is_auth = False
            db.session.commit()
    session.clear()
    return redirect(url_for('index'))
