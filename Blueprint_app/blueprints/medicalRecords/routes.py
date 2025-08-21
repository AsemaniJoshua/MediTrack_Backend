from flask import Blueprint, request, jsonify
from Blueprint_app.app import db
from Blueprint_app.models import MedicalRecord
from datetime import datetime
import uuid
import os
import base64
from flask_login import login_required, current_user

medical_records = Blueprint('medicalRecords', __name__)
MEDICAL_RECORDS_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', 'medical_records')
os.makedirs(MEDICAL_RECORDS_UPLOAD_FOLDER, exist_ok=True)

def save_base64_file(base64_string, upload_folder, filename=None):
    if not base64_string:
        return None, None
    try:
        header, encoded = base64_string.split(',', 1)
        data = base64.b64decode(encoded)
        content_type = header.split(';')[0].split(':')[1]
        
        if not filename:
             file_extension = content_type.split('/')[1]
             filename = f"{str(uuid.uuid4())}.{file_extension}"
             
        file_path = os.path.join(upload_folder, filename)
        
        with open(file_path, "wb") as f:
            f.write(data)
        return file_path, content_type
    except Exception as e:
        print(f"Error decoding or saving file: {e}")
        return None, None

@medical_records.route('/', methods=['POST'])
@login_required
def upload_record():
    data = request.get_json()
    file_path, file_type = save_base64_file(data.get('file'), MEDICAL_RECORDS_UPLOAD_FOLDER)
    
    if not file_path:
        return jsonify({'message': 'Invalid file data'}), 400
    
    new_record = MedicalRecord(
        user_id=current_user.id,
        name=data['name'],
        type=data['type'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        file_type=file_type,
        file_url=file_path
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'message': 'Medical record created successfully', 'record_id': new_record.id}), 201

@medical_records.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_records(user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403
    user_records = MedicalRecord.query.filter_by(user_id=user_id).all()
    output = []
    for record in user_records:
        output.append({
            'id': record.id,
            'userId': record.user_id,
            'name': record.name,
            'type': record.type,
            'date': record.date.isoformat(),
            'fileType': record.file_type,
            'fileUrl': record.file_url,
            'createdAt': record.created_at.isoformat()
        })
    return jsonify(output), 200

@medical_records.route('/<int:record_id>', methods=['PATCH'])
@login_required
def update_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    if record.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 403
    data = request.get_json()
    
    if data.get('file'):
        if record.file_url and os.path.exists(record.file_url):
            os.remove(record.file_url)
        record.file_url, record.file_type = save_base64_file(data.get('file'), MEDICAL_RECORDS_UPLOAD_FOLDER)

    record.name = data.get('name', record.name)
    record.type = data.get('type', record.type)
    
    if data.get('date'):
        record.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
    db.session.commit()
    return jsonify({'message': 'Medical record updated successfully'}), 200

@medical_records.route('/<int:record_id>', methods=['DELETE'])
@login_required
def delete_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    if record.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 403
    if record.file_url and os.path.exists(record.file_url):
        os.remove(record.file_url)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Medical record deleted successfully'}), 204