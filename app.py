from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os

# Configuración de Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:072714@localhost/Test_SaaS'  # Cambia 'user' y 'password'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos
db = SQLAlchemy(app)

# Modelo de la tabla de usuarios
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def home():
    return "Backend Running!"

# Ruta para registrar usuarios (para pruebas)
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Recibe los datos en formato JSON
    username = data.get('username')  # Nombre de usuario
    password = data.get('password')  # Contraseña

    # Verificar si el usuario ya existe
    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    # Encriptar la contraseña
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Crear un nuevo usuario
    new_user = Users(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Ruta para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Buscar usuario en la base de datos
    user = Users.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'user': user.username})

if __name__ == '__main__':
    # Crear las tablas en la base de datos dentro del contexto de la aplicación
    with app.app_context():
        db.create_all()

    app.run(debug=True)
