import logging

from flask import render_template, redirect, url_for, session, flash, request
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app import app, db
from app.criptatre_date import decrypt_data, private_key, public_key, encrypt_data
from app.forms import AddPatientForm, UpdatePatientForm
from app.models import User, Institutie, Pacienti

from datetime import datetime

from app.protocol_psi import see_intersection


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', is_authenticated=session.get('is_authenticated', False))


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

    if session.get('role') == 'admin':
        return render_template('error.html', message="Unauthorized access. You do not have permission to add patients.")

    if session.get('profesie') not in ['administrator', 'doctor', 'asistenta']:
        return render_template('error.html', message="Unauthorized access. You do not have permission to add patients.")

    form = AddPatientForm()

    user = User.query.get(session.get('user_id'))
    institution_id = user.id_institutie
    institution = Institutie.query.get(institution_id)
    hospital_choices = [(institution.nume, institution.nume)]
    form.hospital.choices = hospital_choices
    form.hospital.data = institution.nume
    print(form.hospital.data)

    if form.validate_on_submit():
        try:
            # Criptarea datelor
            encrypted_cnp = encrypt_data(public_key, form.cnp.data)
            encrypted_fisa_medicala = encrypt_data(public_key, form.medical_record.data)
            encrypted_adresa = encrypt_data(public_key, form.address.data)

            new_patient = Pacienti(
                nume=form.last_name.data,
                prenume=form.first_name.data,
                data_nastere=form.birth_date.data.strftime('%Y-%m-%d'),
                varsta=form.age.data,
                cnp=encrypted_cnp,
                sex=form.sex.data,
                fisa_medicala=encrypted_fisa_medicala,
                nr_telefon=form.phone_number.data,
                email=form.email.data,
                adresa=encrypted_adresa,
                id_institutie=institution_id
            )

            db.session.add(new_patient)
            db.session.commit()

            table_name = f'pacienti_{institution.nume}'.replace(" ", "_").replace(".", "")
            query = text(f"""
                INSERT INTO {table_name} (nume, prenume, data_nastere, varsta, cnp, sex, fisa_medicala, nr_telefon, email, adresa, id_pacienti)
                VALUES (:nume, :prenume, :data_nastere, :varsta, :cnp, :sex, :fisa_medicala, :nr_telefon, :email, :adresa, :id_pacienti)
                """)

            # Inserarea în tabelul specific spitalului
            db.session.execute(query, {
                'nume': form.last_name.data,
                'prenume': form.first_name.data,
                'data_nastere': form.birth_date.data.strftime('%Y-%m-%d'),
                'varsta': form.age.data,
                'cnp': encrypted_cnp,
                'sex': form.sex.data,
                'fisa_medicala': encrypted_fisa_medicala,
                'nr_telefon': form.phone_number.data,
                'email': form.email.data,
                'adresa': encrypted_adresa,
                'id_pacienti': new_patient.id
            })
            db.session.commit()

            session['show_success_message'] = True
            flash('Patient added successfully!', 'success')
            return redirect(url_for('add_patient'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error occurred while adding patient: {e}")
            flash('An error occurred while adding the patient. Please try again.', 'danger')
            return redirect(url_for('add_patient'))

    return render_template('add_patient.html', form=form)


@app.route('/view_intersection', methods=['GET', 'POST'])
def view_intersection():
    if not session.get('is_authenticated'):
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))

    not_found_message = "Search for a patient."

    if session.get('role') == 'admin' or session.get('profesie') not in ['administrator', 'doctor', 'asistenta']:
        not_found_message = 'You do not have permission to access patients.'
        return render_template('view_intersection.html', pacient=None, intersection_result=None,
                               numele_spitalului=None, not_found_message=not_found_message)

    search_query = request.args.get('search_query', '').lower()
    pacient = None
    intersection_result = []

    user = User.query.get(session.get('user_id'))
    institution_id = user.id_institutie
    institution = Institutie.query.get(institution_id)
    table_name = f'pacienti_{institution.nume.replace(" ", "_").replace(".", "")}'
    numele_spitalului = institution.nume

    if search_query:
        query = text(f"SELECT id, cnp FROM {table_name}")
        results = db.session.execute(query).fetchall()

        for result in results:
            try:
                decrypted_cnp = decrypt_data(private_key, result.cnp).lower()
                if decrypted_cnp == search_query:
                    pacient_id = result.id
                    pacient_query = text(f"SELECT * FROM {table_name} WHERE id = :id")
                    pacient_data = db.session.execute(pacient_query, {'id': pacient_id}).fetchone()
                    pacient = {
                        'id': pacient_data.id,
                        'nume': pacient_data.nume,
                        'prenume': pacient_data.prenume,
                        'data_nastere': pacient_data.data_nastere,
                        'varsta': pacient_data.varsta,
                        'cnp': decrypted_cnp,
                        'sex': pacient_data.sex,
                        'fisa_medicala': decrypt_data(private_key, pacient_data.fisa_medicala),
                        'nr_telefon': pacient_data.nr_telefon,
                        'email': pacient_data.email,
                        'adresa': decrypt_data(private_key, pacient_data.adresa),
                    }
                    if session.get('profesie') not in ['administrator', 'doctor']:
                        intersection_result = ['You do not have permission to see the intersection.']
                    else:
                        intersection_result = see_intersection(result.cnp, institution_id)
                    break
            except Exception as e:
                logging.error(f"Error decrypting CNP: {e}")
                continue

        if not pacient:
            not_found_message = "Not found."

    return render_template('view_intersection.html', pacient=pacient, intersection_result=intersection_result,
                           numele_spitalului=numele_spitalului, not_found_message=not_found_message)


@app.route('/manage_patients', methods=['GET', 'POST'])
def manage_patients():
    if not session.get('is_authenticated'):
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))

    if session.get('role') == 'admin':
        return render_template('error.html',
                               message="Unauthorized access. You do not have permission to update or delete patients.")

    search_query = request.args.get('search_query', '').lower()

    try:
        user = User.query.get(session.get('user_id'))
        institution_id = user.id_institutie
        institution = Institutie.query.get(institution_id)
        table_name = f'pacienti_{institution.nume.replace(" ", "_").replace(".", "")}'

        query = text(f"SELECT id_pacienti, nume, cnp FROM {table_name}")
        results = db.session.execute(query).fetchall()

        patient_ids = []
        for result in results:
            try:
                decrypted_cnp = decrypt_data(private_key, result.cnp).lower()
                if search_query in decrypted_cnp or search_query in result.nume.lower():
                    patient_ids.append(result.id_pacienti)
            except Exception as e:
                logging.error(f"Error decrypting CNP: {e}")
                continue

        if patient_ids:
            patients = Pacienti.query.filter(Pacienti.id.in_(patient_ids)).all()
        else:
            patients = []

        decrypted_patients = []
        for patient in patients:
            try:
                decrypted_cnp = decrypt_data(private_key, patient.cnp)
                decrypted_fisa_medicala = decrypt_data(private_key, patient.fisa_medicala)
                decrypted_adresa = decrypt_data(private_key, patient.adresa)

                decrypted_patients.append({
                    'id': patient.id,
                    'nume': patient.nume,
                    'prenume': patient.prenume,
                    'data_nastere': patient.data_nastere,
                    'varsta': patient.varsta,
                    'cnp': decrypted_cnp,
                    'sex': patient.sex,
                    'fisa_medicala': decrypted_fisa_medicala,
                    'nr_telefon': patient.nr_telefon,
                    'email': patient.email,
                    'adresa': decrypted_adresa,
                })
            except Exception as e:
                logging.error(f"Error decrypting patient data: {e}")
                continue

    except OperationalError as e:
        flash('Database error occurred. Please try again later.', 'danger')
        decrypted_patients = []

    return render_template('manage_patients.html', patients=decrypted_patients)


@app.route('/update_patient/<int:patient_id>', methods=['GET', 'POST'])
def update_patient(patient_id):
    if not session.get('is_authenticated'):
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))

    if session.get('role') == 'admin':
        return render_template('error.html', message="Unauthorized access. You do not have permission to update "
                                                     "patients.")

    patient = Pacienti.query.get_or_404(patient_id)

    form = UpdatePatientForm()

    if request.method == 'GET':
        form.last_name.data = patient.nume
        form.first_name.data = patient.prenume
        form.birth_date.data = datetime.strptime(patient.data_nastere, '%Y-%m-%d').date()
        form.age.data = patient.varsta
        form.cnp.data = decrypt_data(private_key, patient.cnp)
        form.sex.data = patient.sex
        form.medical_record.data = decrypt_data(private_key, patient.fisa_medicala)
        form.phone_number.data = patient.nr_telefon
        form.email.data = patient.email
        form.address.data = decrypt_data(private_key, patient.adresa)

    if form.validate_on_submit():
        try:
            logging.info(f"Form data on submit: {form.data}")
            # Actualizarea datelor în tabela principală 'pacienti'
            patient.nume = form.last_name.data
            patient.prenume = form.first_name.data
            patient.data_nastere = form.birth_date.data.strftime('%Y-%m-%d')
            patient.varsta = form.age.data
            patient.cnp = encrypt_data(public_key, form.cnp.data)
            patient.sex = form.sex.data
            patient.fisa_medicala = encrypt_data(public_key, form.medical_record.data)
            patient.nr_telefon = form.phone_number.data
            patient.email = form.email.data
            patient.adresa = encrypt_data(public_key, form.address.data)
            db.session.commit()

            # Obține numele spitalului asociat
            institution = Institutie.query.get(patient.id_institutie)
            table_name = f'pacienti_{institution.nume.replace(" ", "_").replace(".", "")}'

            # Actualizarea datelor în tabela specifică spitalului
            update_query = text(f"""
                UPDATE {table_name}
                SET nume = :nume,
                    prenume = :prenume,
                    data_nastere = :data_nastere,
                    varsta = :varsta,
                    cnp = :cnp,
                    sex = :sex,
                    fisa_medicala = :fisa_medicala,
                    nr_telefon = :nr_telefon,
                    email = :email,
                    adresa = :adresa
                WHERE id_pacienti = :id_pacienti
            """)
            db.session.execute(update_query, {
                'nume': form.last_name.data,
                'prenume': form.first_name.data,
                'data_nastere': form.birth_date.data.strftime('%Y-%m-%d'),
                'varsta': form.age.data,
                'cnp': encrypt_data(public_key, form.cnp.data),
                'sex': form.sex.data,
                'fisa_medicala': encrypt_data(public_key, form.medical_record.data),
                'nr_telefon': form.phone_number.data,
                'email': form.email.data,
                'adresa': encrypt_data(public_key, form.address.data),
                'id_pacienti': patient_id
            })
            db.session.commit()

            flash('Patient updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            logging.error(f"An error occurred while updating the patient: {e}")
            flash('An error occurred while updating the patient. Please try again.', 'danger')
        return redirect(url_for('manage_patients'))

    return render_template('update_patient.html', form=form, patient_id=patient_id)


@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    if not session.get('is_authenticated'):
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))

    if session.get('role') == 'admin':
        return render_template('error.html', message="Unauthorized access. You do not have permission to delete "
                                                     "patients.")

    if session.get('profesie') not in ['administrator', 'doctor']:
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
