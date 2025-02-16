from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
import psycopg2
import time

app = Flask(__name__)
socketio = SocketIO(app)  # WebSockets for real-time updates

# PostgreSQL Database Configuration
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "Amoret@2801#"
POSTGRES_DB = "FamousCompanyXYZ"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"

# Function to connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    return conn

# Route for home page
@app.route("/")
def home():
    return render_template("index2.html")  # Ensure index.html exists in the templates folder

# API route to get matches
@app.route("/api/matches")
def get_matches():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Email, Phone, SSN FROM matches")
    matches = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert to JSON format
    match_data = [{
        'name': match[0],
        'email': match[1],
        'phone': match[2],
        'ssn': match[3]
    } for match in matches]

    return jsonify(match_data)

# Background function to send updates to the frontend
def emit_new_matches():
    while True:
        socketio.sleep(5)  # Update every 5 seconds
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Name, Email, Phone, SSN FROM matches")
        matches = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert to JSON format
        match_data = [{
            'name': match[0],
            'email': match[1],
            'phone': match[2],
            'ssn': match[3]
        } for match in matches]

        socketio.emit('update_matches', match_data)

# Start background task when client connects
@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(emit_new_matches)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5001)

