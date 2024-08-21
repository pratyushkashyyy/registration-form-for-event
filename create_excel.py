import sqlite3
from flask import Flask, g
import requests

app = Flask(__name__)

def connect_to_database():
    sql = sqlite3.connect("instance/event_registration.db")
    sql.row_factory = sqlite3.Row
    return sql

def get_database():
    if not hasattr(g, "event_registration_db"):
        g.event_registration_db = connect_to_database()
    return g.event_registration_db

@app.teardown_appcontext
def close_database(error):
    if hasattr(g, "event_registration_db"):
        g.event_registration_db.close()
def create_all():
    try:
        with app.app_context(): 
            db = get_database()
            cursor = db.cursor()
            registrations = cursor.execute("SELECT * FROM registration").fetchall()
        for reg in registrations:
            number = reg['id']
            participant_type = reg['participant_type']
            college_name = reg['college_name']
            event = reg['event']
            team_leader_name = reg['team_leader_name']
            team_name = reg['team_name']
            team_leader_email = reg['team_leader_email']
            team_leader_phone = reg['team_leader_phone']
            team_members = reg['team_members']
            players = reg['players'] or None
            
            data = {
                "number": number,
                "participant_type": participant_type,
                "college_name": college_name,
                "event": event,
                "team_leader_name": team_leader_name,
                "team_name": team_name,
                "team_leader_email": team_leader_email,
                "team_leader_phone": team_leader_phone,
                "team_members": team_members,
                "players": players
            }

            
            response = requests.post("https://hook.us1.make.com/owi87rfcm78bqje2tzdarpxoy4qcoxtw", json=data)
            print(response.text)
    except Exception as e:
        print(f"Error Happened: {e}")


def create(participant_type,college_name,event,team_leader_name,team_leader_email,team_leader_phone,team_name,team_members_str,player_str):
    data = {
                "number": "None",
                "participant_type": participant_type,
                "college_name": college_name,
                "event": event,
                "team_leader_name": team_leader_name,
                "team_name": team_name,
                "team_leader_email": team_leader_email,
                "team_leader_phone": team_leader_phone,
                "team_members": team_members_str,
                "players": player_str
            }

            
    response = requests.post("https://hook.us1.make.com/owi87rfcm78bqje2tzdarpxoy4qcoxtw", json=data)
    print(response.text)
            
    

