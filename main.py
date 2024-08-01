from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get participant type
    participant_type = request.form.get('participant_type')
    college_name = request.form.get('college-name') if participant_type == 'Other' else None

    # Get uploaded files
    id_card = request.files.get('college-id')
    if id_card:
        id_card.save(os.path.join(app.config['UPLOAD_FOLDER'], id_card.filename))

    # Get selected event
    event = request.form.get('event')

    # Get team details
    team_leader_name = request.form.get('name')
    team_name = request.form.get('team_name')
    team_leader_email = request.form.get('email')
    team_leader_phone = request.form.get('number')

    team_members = []
    for i in range(1, 6):  # Assuming maximum team size is 5
        member_name = request.form.get(f'member{i}')
        if member_name:
            team_members.append(member_name)

    # Get UTR number and payment screenshot
    utr_number = request.form.get('utr')
    payment_screenshot = request.files.get('payment-screenshot')
    if payment_screenshot:
        payment_screenshot.save(os.path.join(app.config['UPLOAD_FOLDER'], payment_screenshot.filename))

    # Here you can process the data further, e.g., save to a database or send an email

    # For demonstration, we'll just print the data to the console
    print(f"Participant Type: {participant_type}")
    if college_name:
        print(f"College Name: {college_name}")
    print(f"Event: {event}")
    print(f"Team Leader Name: {team_leader_name}")
    print(f"Team Name: {team_name}")
    print(f"Team Leader Email: {team_leader_email}")
    print(f"Team Leader Phone: {team_leader_phone}")
    print(f"Team Members: {', '.join(team_members)}")
    print(f"UTR Number: {utr_number}")

    # Redirect to a success page or back to the form
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
