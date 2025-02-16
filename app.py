from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import psycopg2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Fetch PostgreSQL credentials from .env
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Change this in production
jwt = JWTManager(app)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    return conn

# Encryption/Decryption functions
def encrypt_data(data: str, secret_key: str) -> str:
    cipher = AES.new(secret_key.encode(), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ct

def decrypt_data(encrypted_data: str, secret_key: str) -> str:
    iv = base64.b64decode(encrypted_data[:24])
    ct = base64.b64decode(encrypted_data[24:])
    cipher = AES.new(secret_key.encode(), AES.MODE_CBC, iv=iv)
    decrypted = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
    return decrypted

def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

# Routes
@app.route('/')
def index():
    return render_template('index.html')  # Render the homepage

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == "valid_user" and password == "valid_password":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/vault/retrieve', methods=['GET'])
@jwt_required()
def retrieve_vault():
    current_user = get_jwt_identity()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted_data FROM company_data WHERE user_id = %s", (current_user,))
    result = cursor.fetchone()

    if result:
        encrypted_data = result[0]
        decrypted_data = decrypt_data(encrypted_data, "your_secret_key")
        return jsonify({"data": decrypted_data})
    else:
        return jsonify({"msg": "No data found!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
