from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import random
import time

app = Flask(__name__)

# Set up your PostgreSQL URI (make sure to replace with actual database info)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/alerts_db'  # replace with your actual database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model for Alerts
class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leak_source = db.Column(db.String(100), nullable=False)
    leak_time = db.Column(db.String(50), nullable=False)

# Route for home page
@app.route("/")
def home():
    return render_template("index.html")

# API route to get alerts
@app.route("/api/alerts")
def get_alerts():
    # Fetch all alerts from PostgreSQL database
    alerts = Alert.query.all()
    alert_data = []
    for alert in alerts:
        alert_data.append({
            'id': alert.id,
            'leak_source': alert.leak_source,
            'leak_time': alert.leak_time
        })
    return jsonify(alert_data)

if __name__ == "_main_":
    app.run(debug=True)