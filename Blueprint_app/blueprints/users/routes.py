from flask import Blueprint, request, jsonify
from Blueprint_app.app import db, bcrypt
from Blueprint_app.models import User
import uuid
import os
import base64
from flask_login import login_user, logout_user, login_required, current_user

users = Blueprint('users', __name__)
# USER_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', 'user_photos')
# os.makedirs(USER_UPLOAD_FOLDER, exist_ok=True)

def save_base64_image(base64_string, upload_folder):
    if not base64_string:
        return None
    try:
        header, encoded = base64_string.split(',', 1)
        data = base64.b64decode(encoded)
        file_extension = header.split(';')[0].split('/')[1]
        
        filename = f"{str(uuid.uuid4())}.{file_extension}"
        file_path = os.path.join(upload_folder, filename)
        
        with open(file_path, "wb") as f:
            f.write(data)
        return filename
    except Exception as e:
        print(f"Error decoding or saving image: {e}")
        return None

@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing email or password'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    # photo_filename = save_base64_image(data.get('photo'), USER_UPLOAD_FOLDER)

    new_user = User(
        name=data.get('name'),
        email=data['email'],
        password_hash=hashed_password,
        # photo_filename=photo_filename,
        emergency_contact=data.get('emergencyContact')
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New user created successfully!', 'user_id': new_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'User registration failed', 'error': str(e)}), 409

@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user and bcrypt.check_password_hash(user.password_hash, data.get('password')):
        login_user(user)
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@users.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@users.route('/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        # 'photoFilename': user.photo_filename,
        'emergencyContact': user.emergency_contact,
        'createdAt': user.created_at.isoformat(),
        'updatedAt': user.updated_at.isoformat()
    }), 200

@users.route('/<int:user_id>', methods=['PATCH'])
@login_required
def update_user(user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    # if data.get('photo'):
    #     if user.photo_filename and os.path.exists(os.path.join(USER_UPLOAD_FOLDER, user.photo_filename)):
    #         os.remove(os.path.join(USER_UPLOAD_FOLDER, user.photo_filename))
    #     user.photo_filename = save_base64_image(data.get('photo'), USER_UPLOAD_FOLDER)
    
    user.name = data.get('name', user.name)
    user.emergency_contact = data.get('emergencyContact', user.emergency_contact)
    
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200


