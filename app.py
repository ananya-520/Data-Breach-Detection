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
    return render_template("index.html")

# API route to get alerts
@app.route("/api/alerts")
def get_alerts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, company_name, spike_amount, affected_time, alert_message, timestamp FROM brokerage_spike_alert")
    alerts = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert the timestamp to a string in a readable format
    alert_data = [{
        'id': alert[0],
        'company_name': alert[1],
        'spike_amount': alert[2],
        'affected_time': alert[3],
        'alert_message': alert[4],
        'timestamp': alert[5].strftime('%Y-%m-%d %H:%M:%S')  # Format datetime to string
    } for alert in alerts]

    return jsonify(alert_data)

# Background function to send updates to the frontend
def emit_new_alerts():
    while True:
        socketio.sleep(5)  # Update every 5 seconds
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, company_name, spike_amount, affected_time, alert_message, timestamp FROM brokerage_spike_alert")
        alerts = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert the timestamp to a string in a readable format
        alert_data = [{
            'id': alert[0],
            'company_name': alert[1],
            'spike_amount': alert[2],
            'affected_time': alert[3],
            'alert_message': alert[4],
            'timestamp': alert[5].strftime('%Y-%m-%d %H:%M:%S')  # Format datetime to string
        } for alert in alerts]

        socketio.emit('update_alerts', alert_data)

# Start background task when client connects
@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(emit_new_alerts)

if __name__ == "__main__":
    socketio.run(app, debug=True)
