import random
import datetime
import logging
from sqlalchemy import text
from app import db, app
from app.models import Pacienti, Institutie
from app.criptatre_date import encrypt_data, public_key, decrypt_data, private_key


def generate_cnp():
    # Generare componenta sex și secol
    sex = random.choice([1, 2, 5, 6])  # 1, 2 pentru 1900-1999; 5, 6 pentru 2000-2099
    year = random.randint(1950, 2020)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Pentru simplitate, toate lunile au maxim 28 de zile

    if sex in [1, 2]:
        year_part = year - 1900
    else:
        year_part = year - 2000

    county = random.randint(1, 52)
    order_number = random.randint(0, 999)

    cnp_without_control = f"{sex}{year_part:02}{month:02}{day:02}{county:02}{order_number:03}"

    # Asigură-te că cnp_without_control este corect și numeric
    cnp_without_control = ''.join(filter(str.isdigit, cnp_without_control))
    assert len(cnp_without_control) == 12, f"CNP incomplet: {cnp_without_control}"

    control_digit = generate_control_digit(cnp_without_control)

    return f"{cnp_without_control}{control_digit}"

def generate_control_digit(cnp_without_control):
    weights = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    checksum = sum(int(cnp_without_control[i]) * weights[i] for i in range(12))
    control_digit = checksum % 11
    return control_digit if control_digit < 10 else 1

def generate_random_patient_data():
    first_names = ['Stefania','Delia','Amalia','Octavian', 'George', 'Mihai', 'Denis', 'Diana-Maria', 'Marcel',
                   'Rares-Ioanid', 'Ion', 'Maria','Andrei', 'Ana', 'Elena', 'Cristina', 'Radu', 'Irina','Cecilia',
                   'Alexandru', 'Gabriela', 'Robert', 'Victor', 'Carmen', 'Otilia', 'David']
    last_names = ['Deleanu','Cucos','Curmei','Harton','Iacob','Nestian', 'Scinteie', 'Galatianu', 'Duluta', 'Chelea',
                  'Carp', 'Popescu', 'Sima', 'Grosu', 'Silitra', 'Stanciu', 'Andrusca', 'Iorga',
                  'Musteata', 'Lozba', 'Pichiu', 'Balan', 'Pandeli']

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    birth_date = datetime.date(year=random.randint(1950, 2000), month=random.randint(1, 12), day=random.randint(1, 28))
    # Generăm o vârstă aleatorie pentru ultimul consult
    age_at_last_consult = random.choice(((datetime.date.today().year - birth_date.year) % 18))
    cnp = generate_cnp()
    sex = 'M' if int(cnp[0]) % 2 == 1 else 'F'
    medical_record = f"Fisa medicala {random.randint(1, 100)}"
    phone_number = f"07{random.randint(10000000, 99999999)}"
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    address = f"Strada {random.choice(last_names)}, Nr. {random.randint(1, 100)}, {random.choice(['Bucuresti', 'Cluj', 'Timisoara', 'Iasi'])}"

    return {
        'last_name': last_name,
        'first_name': first_name,
        'birth_date': birth_date.strftime('%Y-%m-%d'),
        'age': age_at_last_consult,
        'cnp': cnp,
        'sex': sex,
        'medical_record': medical_record,
        'phone_number': phone_number,
        'email': email,
        'address': address
    }

def add_patient_to_db(patient_data, hospitals):
    for hospital_name in hospitals:
        try:
            # Obține informațiile instituției
            institution = Institutie.query.filter_by(nume=hospital_name).first()
            if not institution:
                logging.error(f"Institution not found: {hospital_name}")
                continue

            # Criptarea datelor
            encrypted_cnp = encrypt_data(public_key, patient_data['cnp'])
            encrypted_fisa_medicala = encrypt_data(public_key, patient_data['medical_record'])
            encrypted_adresa = encrypt_data(public_key, patient_data['address'])

            # Verifică dacă pacientul există deja în baza de date
            existing_patient = Pacienti.query.filter_by(cnp=encrypted_cnp, id_institutie=institution.id).first()
            if existing_patient:
                logging.info(
                    f"Patient {patient_data['first_name']} {patient_data['last_name']} already exists in {hospital_name}.")
                continue

            # Crearea noului pacient
            new_patient = Pacienti(
                nume=patient_data['last_name'],
                prenume=patient_data['first_name'],
                data_nastere=patient_data['birth_date'],
                varsta=patient_data['age'],
                cnp=encrypted_cnp,
                sex=patient_data['sex'],
                fisa_medicala=encrypted_fisa_medicala,
                nr_telefon=patient_data['phone_number'],
                email=patient_data['email'],
                adresa=encrypted_adresa,
                id_institutie=institution.id
            )

            # Adaugă noul pacient în baza de date
            db.session.add(new_patient)
            db.session.commit()

            # Pregătește numele tabelului specific spitalului
            table_name = f'pacienti_{institution.nume}'.replace(" ", "_").replace(".", "")
            print(table_name)
            query = text(f"""
                INSERT INTO {table_name} (nume, prenume, data_nastere, varsta, cnp, sex, fisa_medicala, nr_telefon, email, adresa, id_pacienti)
                VALUES (:nume, :prenume, :data_nastere, :varsta, :cnp, :sex, :fisa_medicala, :nr_telefon, :email, :adresa, :id_pacienti)
            """)

            # Inserarea în tabelul specific spitalului
            db.session.execute(query, {
                'nume': patient_data['last_name'],
                'prenume': patient_data['first_name'],
                'data_nastere': patient_data['birth_date'],
                'varsta': patient_data['age'],
                'cnp': encrypted_cnp,
                'sex': patient_data['sex'],
                'fisa_medicala': encrypted_fisa_medicala,
                'nr_telefon': patient_data['phone_number'],
                'email': patient_data['email'],
                'adresa': encrypted_adresa,
                'id_pacienti': new_patient.id
            })
            db.session.commit()

            logging.info(
                f"Patient {patient_data['first_name']} {patient_data['last_name']} added successfully to {hospital_name}.")

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error occurred while adding patient: {e}")

def list_existing_institutions():
    institutions = Institutie.query.all()
    for institution in institutions:
        logging.info(f"Institution found: {institution.nume}")
def get_patient_data(hospital_name, id_patient):
    other_table_name = f'pacienti_{hospital_name.replace(" ", "_").replace(".", "")}'
    query = text(f"SELECT * FROM {other_table_name} where id = {id_patient}")
    results = db.session.execute(query).fetchall()
    for result in results:
        if result:
            decrypted_cnp = decrypt_data(private_key, result.cnp)
            decrypted_address = decrypt_data(private_key, result.adresa)
            decrypted_fisa_medicala = decrypt_data(private_key, result.fisa_medicala)

            decrypted_data = {
                'id': result.id_pacienti,
                'nume': result.nume,
                'prenume': result.prenume,
                'data_nastere': result.data_nastere,
                'varsta': result.varsta,
                'cnp': decrypted_cnp,
                'sex': result.sex,
                'fisa_medicala': decrypted_fisa_medicala,
                'nr_telefon': result.nr_telefon,
                'email': result.email,
                'adresa': decrypted_address
            }
            return decrypted_data


hospital_names = [
    'Providenta',
    'Spitalul de copii Sf Maria',
    'Spitalul Clinic Judetean De Urgente Sf Spiridon',
    'Arcadia',
    'Spitalul Clinic CFR',
    'Parhon'
]

with app.app_context():
    list_existing_institutions()


with app.app_context():
    decrypted_patient_data = get_patient_data(hospital_names[1], 7)
    if decrypted_patient_data:
        print(decrypted_patient_data)
