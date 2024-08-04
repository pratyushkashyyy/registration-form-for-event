from flask import Flask, request, render_template, redirect, url_for, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_registration.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'


db = SQLAlchemy(app)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_type = db.Column(db.String(50))
    college_name = db.Column(db.String(100))
    event = db.Column(db.String(100))
    team_leader_name = db.Column(db.String(100))
    team_name = db.Column(db.String(100))
    team_leader_email = db.Column(db.String(100))
    team_leader_phone = db.Column(db.String(20))
    team_members = db.Column(db.String(500))
    players = db.Column(db.String(500))
    utr_number = db.Column(db.String(100))
    id_card_filename = db.Column(db.String(200))
    payment_screenshot_filename = db.Column(db.String(200))

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    participant_type = request.form.get('participant_type')
    college_name = request.form.get('college-name') if participant_type == 'Other' else None

    id_card = request.files.get('college_id')
    id_card_filename = None
    if id_card:
        try:
            id_card_filename = str(uuid.uuid4()) + "_" + id_card.filename
            id_card_path = os.path.join(app.config['UPLOAD_FOLDER'], id_card_filename)
            print(f"Saving college ID to: {id_card_path}")
            id_card.save(id_card_path)
        except Exception as e:
            print(f"Failed to save college ID: {e}")


    event = request.form.get('event')
    team_leader_name = request.form.get('name')
    team_name = request.form.get('team_name')
    team_leader_email = request.form.get('email')
    team_leader_phone = request.form.get('number')

    team_members = []
    for i in range(1, 6):
        member_name = request.form.get(f'team_member_{i}')
        if member_name:
            team_members.append(member_name)
    team_members_str = ', '.join(team_members)

    players = []
    for i in range(1,6):
        player_uid = request.form.get(f'player{i}_uid')
        if player_uid:
            players.append(player_uid)
    player_str = ', '.join(players)

    utr_number = request.form.get('utr')
    payment_screenshot = request.files.get('payment_screenshot')
    payment_screenshot_filename = None
    if payment_screenshot:
        payment_screenshot_filename = str(uuid.uuid4()) + "_" + payment_screenshot.filename
        payment_screenshot.save(os.path.join(app.config['UPLOAD_FOLDER'], payment_screenshot_filename))

    registration = Registration(
        participant_type=participant_type,
        college_name=college_name,
        event=event,
        team_leader_name=team_leader_name,
        team_name=team_name,
        team_leader_email=team_leader_email,
        team_leader_phone=team_leader_phone,
        team_members=team_members_str,
        players = player_str,
        utr_number=utr_number,
        id_card_filename=id_card_filename,
        payment_screenshot_filename=payment_screenshot_filename
    )
    db.session.add(registration)
    db.session.commit()

    return render_template('success.html')



def send_email_to_registration(registration):
    smtp_server = 'smtp.gmail.com'
    port = 587
    login = 'your_email@gmail.com'
    password = 'your_password'
    sender_email = 'your_email@gmail.com'
    recipient_email = registration.team_leader_email
    subject = 'Registration Confirmation'
    body = f"""
    Dear {registration.team_leader_name},

    Thank you for registering for {registration.event}.
    
    Best regards,
    Event Team
    """

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(login, password)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()

@app.route('/admin/send_email/<int:id>', methods=['POST'])
def send_email(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    registration = Registration.query.get_or_404(id)
    send_email_to_registration(registration)
    flash('Email has been sent', 'success')

    return redirect(url_for('admin'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials, please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    registrations = Registration.query.all()
    return render_template('admin.html', registrations=registrations)

@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_entry(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    registration = Registration.query.get_or_404(id)
    if registration.id_card_filename:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], registration.id_card_filename))
        except OSError as e:
            print(f"Error: {e.strerror} - {e.filename}")

    if registration.payment_screenshot_filename:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], registration.payment_screenshot_filename))
        except OSError as e:
            print(f"Error: {e.strerror} - {e.filename}")

    db.session.delete(registration)
    db.session.commit()
    flash('Registration has been deleted', 'success')
    
    return redirect(url_for('admin'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
