from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash
from app import db


class Institutie(db.Model):
    __tablename__ = 'institutii'

    id = Column(Integer, primary_key=True)
    nume = Column(String(255))
    adresa = Column(String(255))
    users = relationship("User", back_populates="institutie")
    pacienti = relationship("Pacienti", back_populates="institutie")

    def __repr__(self):
        return f'<Institutie {self.nume}>'


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nume = Column(String(255))
    prenume = Column(String(255))
    email = Column(String(255), unique=True)
    profesie = Column(String(255))
    parola = Column(String(255))
    is_auth = Column(Boolean, default=False)
    role = Column(String(50), default='user')
    id_institutie = Column(Integer, ForeignKey('institutii.id'))
    institutie = relationship("Institutie", back_populates="users")

    def check_password(self, password):
        return check_password_hash(self.parola, password)

    def __repr__(self):
        return f'<User {self.nume} {self.prenume}>'


class Pacienti(db.Model):
    __tablename__ = 'pacienti'

    id = Column(Integer, primary_key=True)
    nume = Column(String(255))
    prenume = Column(String(255))
    data_nastere = Column(String(255))
    varsta = Column(Integer)
    cnp = Column(String(255))
    sex = Column(String(255))
    fisa_medicala = Column(String(255))
    nr_telefon = Column(String(255))
    email = Column(String(255), unique=True)
    adresa = Column(String(255))
    id_institutie = Column(Integer, ForeignKey('institutii.id'))
    institutie = relationship("Institutie", back_populates="pacienti")

    def __repr__(self):
        return f'<Pacient id={self.id} nume={self.nume} prenume={self.prenume} data_nastere={self.data_nastere} varsta={self.varsta} cnp={self.cnp} sex={self.sex} fisa_medicala={self.fisa_medicala} nr_telefon={self.nr_telefon} email={self.email} adresa={self.adresa}>'

def create_pacienti_tables():
    hospitals = Institutie.query.all()
    for hospital in hospitals:
        table_name = f'pacienti_{hospital.nume.replace(" ", "_").replace(".", "")}'
        query = text(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            nume VARCHAR(255),
            prenume VARCHAR(255),
            data_nastere VARCHAR(255),
            varsta INTEGER,
            cnp VARCHAR(255) UNIQUE,
            sex VARCHAR(255),
            fisa_medicala VARCHAR(255),
            nr_telefon VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            adresa VARCHAR(255),
            id_pacienti INTEGER REFERENCES pacienti(id)
        );
        """)
        db.session.execute(query)
    db.session.commit()
