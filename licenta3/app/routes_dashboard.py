from flask import render_template, redirect, url_for, session, flash, request
from sqlalchemy.exc import OperationalError
from app import app, db
from app.forms import UpdateUserForm
from app.models import User, Institutie


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('is_authenticated') and session.get('role') != 'admin':
        flash('You need to be logged in as an admin to access this page.', 'danger')
        return redirect(url_for('login'))

    search_query = request.args.get('search_query', '')

    try:
        if search_query:
            users = User.query.filter(
                (User.nume.ilike(f"%{search_query}%") | User.email.ilike(f"%{search_query}%")) & (User.role != 'admin')
            ).all()
        else:
            users = User.query.filter(User.role != 'admin').all()
    except OperationalError as e:
        flash('Database error occurred. Please try again later.', 'danger')
        users = []

    return render_template('dashboard.html', users=users)


@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    if not session.get('is_authenticated') or session.get('role') != 'admin':
        flash('You need to be logged in as an admin to access this page.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    form = UpdateUserForm()

    institutii = Institutie.query.all()
    hospital_choices = [(institutie.nume, institutie.nume) for institutie in institutii]
    form.hospital.choices = hospital_choices

    if request.method == 'GET':
        form.last_name.data = user.nume
        form.first_name.data = user.prenume
        form.email.data = user.email
        form.profession.data = user.profesie
        form.hospital.data = Institutie.query.get(user.id_institutie).nume

    if form.validate_on_submit():
        try:
            user.nume = form.last_name.data
            user.prenume = form.first_name.data
            user.email = form.email.data
            user.profesie = form.profession.data

            institutie = Institutie.query.filter_by(nume=form.hospital.data).first()
            if not institutie:
                flash('Selected hospital does not exist. Please choose a valid hospital.', 'error')
                return redirect(url_for('update_user', user_id=user_id))

            user.id_institutie = institutie.id
            db.session.commit()
            flash('User updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the user. Please try again.', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('update_user.html', form=form, user_id=user_id)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('is_authenticated') and session.get('role') != 'admin':
        flash('You need to be logged in as an admin to access this page.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the user. Please try again.', 'danger')

    return redirect(url_for('dashboard'))
