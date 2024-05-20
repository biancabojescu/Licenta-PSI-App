import logging

from flask import render_template, redirect, url_for, session, flash, request
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddPatientForm, SearchForm, UpdatePatientForm
from app.models import User, Institutie, Pacienti
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', is_authenticated=session.get('is_authenticated', False))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['is_authenticated'] = True
            session['role'] = user.role
            session['profesie'] = user.profesie
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET'])
def register():
    institutii = Institutie.query.all()
    hospital_choices = [(institutie.nume, institutie.nume) for institutie in institutii]

    form = RegistrationForm()
    form.hospital.choices = hospital_choices

    return render_template('register.html', title='Register', form=form)


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


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.parola, form.password.data):
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
            nume=form.first_name.data,
            prenume=form.last_name.data,
            email=form.email.data,
            profesie=form.profession.data,
            parola=hashed_password,
            is_auth=False,
            role='user',
            id_institutie=institutie.id
        )
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, registration successful!', 'success')
        return redirect(url_for('login'))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f"{fieldName}: {err}", 'error')
    return render_template('register.html', title='Register', form=form)


@app.route('/services')
def services():
    if not session.get('is_authenticated'):
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))
    return render_template('services.html')


@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if not session.get('is_authenticated'):
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))

    if session.get('profesie') not in ['administrator', 'doctor', 'asistenta'] or session.get('role') != 'admin':
        return render_template('error.html', message="Unauthorized access. You do not have permission to add patients.")

    form = AddPatientForm()
    institutii = Institutie.query.all()
    hospital_choices = [(institutie.nume, institutie.nume) for institutie in institutii]
    form.hospital.choices = hospital_choices

    if form.validate_on_submit():
        try:
            institutie = Institutie.query.filter_by(nume=form.hospital.data).first()
            new_patient = Pacienti(
                nume=form.last_name.data,
                prenume=form.first_name.data,
                data_nastere=form.birth_date.data.strftime('%Y-%m-%d'),
                varsta=form.age.data,
                cnp=form.cnp.data,
                sex=form.sex.data,
                fisa_medicala=form.medical_record.data,
                nr_telefon=form.phone_number.data,
                email=form.email.data,
                adresa=form.address.data,
                id_institutie=institutie.id
            )
            db.session.add(new_patient)
            db.session.commit()

            # Adăugăm pacientul în tabela specifică spitalului
            table_name = f'pacienti_{form.hospital.data}'.replace(" ", "_").replace(".", "")
            query = text(f"""
                INSERT INTO {table_name} (nume, prenume, data_nastere, varsta, cnp, sex, fisa_medicala, nr_telefon, email, adresa, id_pacienti)
                VALUES (:nume, :prenume, :data_nastere, :varsta, :cnp, :sex, :fisa_medicala, :nr_telefon, :email, :adresa, :id_pacienti)
                """)
            db.session.execute(query, {
                'nume': form.first_name.data,
                'prenume': form.last_name.data,
                'data_nastere': form.birth_date.data.strftime('%Y-%m-%d'),
                'varsta': form.age.data,
                'cnp': form.cnp.data,
                'sex': form.sex.data,
                'fisa_medicala': form.medical_record.data,
                'nr_telefon': form.phone_number.data,
                'email': form.email.data,
                'adresa': form.address.data,
                'id_pacienti': new_patient.id
            })
            db.session.commit()

            session['show_success_message'] = True
            return redirect(url_for('add_patient'))
        except Exception as e:
            db.session.rollback()
            session['show_error_message'] = True
            return redirect(url_for('add_patient'))

    return render_template('add_patient.html', form=form)


@app.route('/view_intersection')
def view_intersection():
    if not session.get('is_authenticated'):
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))

    if session.get('profesie') not in ['administrator', 'doctor'] or session.get('role') != 'admin':
        return render_template('error.html',
                               message="Unauthorized access. You do not have permission to view intersections.")

    return render_template('view_intersection.html')


@app.route('/manage_patients', methods=['GET', 'POST'])
def manage_patients():
    if not session.get('is_authenticated'):
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))

    search_query = request.args.get('search_query', '')

    try:
        if session.get('role') == 'admin':
            if search_query:
                patients = Pacienti.query.filter(
                    Pacienti.nume.ilike(f"%{search_query}%") | Pacienti.cnp.ilike(f"%{search_query}%")
                ).all()
            else:
                patients = Pacienti.query.all()
        else:
            user = User.query.get(session.get('user_id'))
            institution_id = user.id_institutie
            institution = Institutie.query.get(institution_id)
            table_name = f'pacienti_{institution.nume.replace(" ", "_").replace(".", "")}'
            if search_query:
                query = text(f"SELECT * FROM {table_name} WHERE nume LIKE :search_query OR cnp LIKE :search_query")
                patients = db.session.execute(query, {'search_query': f"%{search_query}%"}).fetchall()
            else:
                query = text(f"SELECT * FROM {table_name}")
                patients = db.session.execute(query).fetchall()
    except OperationalError as e:
        flash('Database error occurred. Please try again later.', 'danger')
        patients = []

    return render_template('manage_patients.html', patients=patients)


import logging

import logging


@app.route('/update_patient/<int:patient_id>', methods=['GET', 'POST'])
def update_patient(patient_id):
    if not session.get('is_authenticated'):
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))

    patient = Pacienti.query.get_or_404(patient_id)
    logging.info(f"Patient data before form population: {patient}")

    form = UpdatePatientForm(obj=patient)
    logging.info(f"Form data after population: {form.data}")

    if form.validate_on_submit():
        try:
            logging.info(f"Form data on submit: {form.data}")
            patient.nume = form.last_name.data
            patient.prenume = form.first_name.data
            patient.data_nastere = form.birth_date.data.strftime('%Y-%m-%d')
            patient.varsta = form.age.data
            patient.cnp = form.cnp.data
            patient.sex = form.sex.data
            patient.fisa_medicala = form.medical_record.data
            patient.nr_telefon = form.phone_number.data
            patient.email = form.email.data
            patient.adresa = form.address.data
            db.session.commit()
            flash('Patient updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error occurred while updating patient: {e}")
            flash('An error occurred while updating the patient. Please try again.', 'danger')
        return redirect(url_for('manage_patients'))

    return render_template('update_patient.html', form=form, patient_id=patient_id)


@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    if not session.get('is_authenticated'):
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))

    if session.get('profession') not in ['administrator', 'doctor'] and session.get('role') != 'admin':
        flash('You do not have permission to delete patients.', 'danger')
        return redirect(url_for('manage_patients'))

    patient = Pacienti.query.get_or_404(patient_id)
    try:
        institution_id = patient.id_institutie
        institution = Institutie.query.get(institution_id)
        table_name = f'pacienti_{institution.nume.replace(" ", "_").replace(".", "")}'
        query = text(f"DELETE FROM {table_name} WHERE id_pacienti = :patient_id")
        db.session.execute(query, {'patient_id': patient_id})
        db.session.commit()

        db.session.delete(patient)
        db.session.commit()
        flash('Patient deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error occurred while deleting patient: {e}")
        flash('An error occurred while deleting the patient. Please try again.', 'danger')

    return redirect(url_for('manage_patients'))


@app.route('/search_patient', methods=['POST'])
def search_patient():
    search_query = request.form.get('search_query')
    return redirect(url_for('manage_patients', search_query=search_query))


@app.route('/dashboard')
def dashboard():
    if not session.get('is_authenticated') or session.get('role') != 'admin':
        abort(403)
    return render_template('dashboard.html')
