from flask import Blueprint, request, jsonify
from Blueprint_app.app import db
from Blueprint_app.models import Appointment
from datetime import datetime
import uuid
from flask_login import login_required, current_user

appointments = Blueprint('appointments', __name__)

@appointments.route('/', methods=['POST'])
@login_required
def add_appointment():
    data = request.get_json()
    new_appointment = Appointment(
        user_id=current_user.id,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        time=data['time'],
        location=data['location'],
        doctor=data['doctor'],
        notes=data.get('notes'),
        status=data['status']
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment scheduled successfully', 'appointment_id': new_appointment.id}), 201

@appointments.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_appointments(user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403
    user_appointments = Appointment.query.filter_by(user_id=user_id).all()
    output = []
    for appt in user_appointments:
        output.append({
            'id': appt.id,
            'userId': appt.user_id,
            'date': appt.date.isoformat(),
            'time': appt.time,
            'location': appt.location,
            'doctor': appt.doctor,
            'notes': appt.notes,
            'status': appt.status
        })
    return jsonify(output), 200

@appointments.route('/<int:appointment_id>', methods=['PATCH'])
@login_required
def update_appointment(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    if appt.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 403
    data = request.get_json()
    appt.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    appt.time = data['time']
    appt.location = data['location']
    appt.doctor = data['doctor']
    appt.notes = data['notes']
    appt.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Appointment updated successfully'}), 200

@appointments.route('/<int:appointment_id>', methods=['DELETE'])
@login_required
def delete_appointment(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    if appt.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 403
    db.session.delete(appt)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted successfully'}), 204