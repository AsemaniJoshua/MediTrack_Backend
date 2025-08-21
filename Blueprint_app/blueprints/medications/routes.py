from flask import Blueprint, request, jsonify
from Blueprint_app.app import db
from Blueprint_app.models import Medication
from datetime import datetime
import uuid
import os
import base64
from flask_login import login_required, current_user

medications = Blueprint('medications', __name__)
MEDICATION_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', 'medication_photos')
os.makedirs(MEDICATION_UPLOAD_FOLDER, exist_ok=True)

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

@medications.route('/', methods=['POST'])
@login_required
def add_medication():
    data = request.get_json()
    photo_filename = save_base64_image(data.get('photo'), MEDICATION_UPLOAD_FOLDER)

    new_medication = Medication(
        user_id=current_user.id,
        name=data['name'],
        dosage=data['dosage'],
        frequency=data['frequency'],
        start_date=datetime.strptime(data['startDate'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['endDate'], '%Y-%m-%d').date(),
        time=data['time'],
        photo_filename=photo_filename
    )
    db.session.add(new_medication)
    db.session.commit()
    return jsonify({'message': 'Medication added successfully', 'medication_id': new_medication.id}), 201

@medications.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_medications(user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403
    user_medications = Medication.query.filter_by(user_id=user_id).all()
    output = []
    for med in user_medications:
        output.append({
            'id': med.id,
            'userId': med.user_id,
            'name': med.name,
            'dosage': med.dosage,
            'frequency': med.frequency,
            'startDate': med.start_date.isoformat(),
            'endDate': med.end_date.isoformat(),
            'time': med.time,
            'photoFilename': med.photo_filename
        })
    return jsonify(output), 200

@medications.route('/<int:medication_id>', methods=['PATCH'])
@login_required
def update_medication(medication_id):
    med = Medication.query.get_or_404(medication_id)
    if med.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 403
    data = request.get_json()
    
    if data.get('photo'):
        if med.photo_filename and os.path.exists(os.path.join(MEDICATION_UPLOAD_FOLDER, med.photo_filename)):
            os.remove(os.path.join(MEDICATION_UPLOAD_FOLDER, med.photo_filename))
        med.photo_filename = save_base64_image(data.get('photo'), MEDICATION_UPLOAD_FOLDER)
    
    med.name = data.get('name', med.name)
    med.dosage = data.get('dosage', med.dosage)
    med.frequency = data.get('frequency', med.frequency)
    db.session.commit()
    return jsonify({'message': 'Medication updated successfully'}), 200

@medications.route('/<int:medication_id>', methods=['DELETE'])
@login_required
def delete_medication(medication_id):
    med = Medication.query.get_or_404(medication_id)
    if med.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 403
    if med.photo_filename and os.path.exists(os.path.join(MEDICATION_UPLOAD_FOLDER, med.photo_filename)):
        os.remove(os.path.join(MEDICATION_UPLOAD_FOLDER, med.photo_filename))
    db.session.delete(med)
    db.session.commit()
    return jsonify({'message': 'Medication deleted successfully'}), 204