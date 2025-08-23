# mediTrack Backend API Documentation

Welcome to the mediTrack backend API documentation. This guide provides all the necessary information for a frontend developer to interact with the API endpoints.

Created By Joshua Asemani

> **Note:** All API endpoints are prefixed with `https://meditrack-backend-fplg.onrender.com`.

---

## Table of Contents

1. [Core Endpoints](#core-endpoints)
2. [Users Endpoints](#users-endpoints)
3. [Medications Endpoints](#medications-endpoints)
4. [Appointments Endpoints](#appointments-endpoints)
5. [Medical Records Endpoints](#medical-records-endpoints)

---

## Core Endpoints

### `GET /`
**Description:** A simple health check to ensure the API is running.

**Request Body:** None

**Response Body:**
```json
{
    "message": "Welcome to the mediTrack API! The system is operational."
}
```

---

## Users Endpoints

### `POST /api/v1/users/register`
**Description:** Creates a new user account.

**Request Body:**
```json
{
    "name": "string",
    "email": "string",
    "password": "string",
    "emergencyContact": "string"
}
```

**Response Body:**
```json
{
    "message": "New user created successfully!",
    "user_id": 1
}
```

---

### `POST /api/v1/users/login`
**Description:** Authenticates a user.

**Request Body:**
```json
{
    "email": "string",
    "password": "string"
}
```

**Response Body:**
```json
{
    "message": "Login successful",
    "user_id": 1
}
```

---

### `POST /api/v1/users/logout`
**Description:** Logs out the current user.

**Request Body:** None

**Response Body:**
```json
{
    "message": "Logged out successfully"
}
```

---

### `GET /api/v1/users/<user_id>`
**Description:** Retrieves a single user's details by their ID.

**Request Body:** None

**Response Body:**
```json
{
    "createdAt": "string (ISO 8601)",
    "email": "string",
    "emergencyContact": "string",
    "id": 1,
    "name": "string",
    "photoFilename": "string",
    "updatedAt": "string (ISO 8601)"
}
```

---

### `PATCH /api/v1/users/<user_id>`
**Description:** Updates an existing user's details. Only include the fields you wish to update.

**Request Body:**
```json
{
    "name": "string",
    "emergencyContact": "string"
}
```

**Response Body:**
```json
{
    "message": "User updated successfully"
}
```

---

## Medications Endpoints

### `POST /api/v1/medications`
**Description:** Adds a new medication for a user.

**Request Body:**
```json
{
    "userId": 1,
    "name": "string",
    "dosage": "string",
    "frequency": "string",
    "startDate": "YYYY-MM-DD",
    "endDate": "YYYY-MM-DD",
    "time": "string"
}
```

**Response Body:**
```json
{
    "message": "Medication added successfully",
    "medication_id": 1
}
```

---

### `GET /api/v1/medications/user/<user_id>`
**Description:** Retrieves all medications associated with a specific user.

**Request Body:** None

**Response Body:**
```json
[
    {
        "id": 1,
        "userId": 1,
        "name": "string",
        "dosage": "string",
        "frequency": "string",
        "startDate": "YYYY-MM-DD",
        "endDate": "YYYY-MM-DD",
        "time": "string",
        "photoFilename": "string"
    }
]
```

---

### `PATCH /api/v1/medications/<medication_id>`
**Description:** Updates a specific medication. Only include the fields you wish to update.

**Request Body:**
```json
{
    "name": "string",
    "dosage": "string",
    "frequency": "string"
}
```

**Response Body:**
```json
{
    "message": "Medication updated successfully"
}
```

---

### `DELETE /api/v1/medications/<medication_id>`
**Description:** Deletes a specific medication.

**Request Body:** None

**Response Body:**
```json
{
    "message": "Medication deleted successfully"
}
```

---

### `GET /api/v1/medications/allmedications`
**Description:** Retrieves all medications for all users.

**Request Body:** None

**Response Body:**
```json
[
    {
        "id": 1,
        "userId": 1,
        "name": "string",
        "dosage": "string",
        "frequency": "string",
        "startDate": "YYYY-MM-DD",
        "endDate": "YYYY-MM-DD",
        "time": "string"
    }
]
```

---

## Appointments Endpoints

### `POST /api/v1/appointments`
**Description:** Schedules a new appointment for a user.

**Request Body:**
```json
{
    "userId": 1,
    "date": "YYYY-MM-DD",
    "time": "string",
    "location": "string",
    "doctor": "string",
    "notes": "string"
}
```

**Response Body:**
```json
{
    "message": "Appointment scheduled successfully",
    "appointment_id": 1
}
```

---

### `GET /api/v1/appointments/user/<user_id>`
**Description:** Retrieves all appointments for a specific user.

**Request Body:** None

**Response Body:**
```json
[
    {
        "id": 1,
        "userId": 1,
        "date": "YYYY-MM-DD",
        "time": "string",
        "location": "string",
        "doctor": "string",
        "notes": "string"
    }
]
```

---

### `PATCH /api/v1/appointments/<appointment_id>`
**Description:** Updates a specific appointment. Only include the fields you wish to update.

**Request Body:**
```json
{
    "date": "YYYY-MM-DD",
    "time": "string",
    "location": "string",
    "doctor": "string",
    "notes": "string"
}
```

**Response Body:**
```json
{
    "message": "Appointment updated successfully"
}
```

---

### `DELETE /api/v1/appointments/<appointment_id>`
**Description:** Deletes a specific appointment.

**Request Body:** None

**Response Body:**
```json
{
    "message": "Appointment deleted successfully"
}
```

---

### `GET /api/v1/appointments/allappointments`
**Description:** Retrieves all appointments for all users.

**Request Body:** None

**Response Body:**
```json
[
    {
        "id": 1,
        "userId": 1,
        "date": "YYYY-MM-DD",
        "time": "string",
        "location": "string",
        "doctor": "string",
        "notes": "string"
    }
]
```

---

## Medical Records Endpoints

### `POST /api/v1/medical_records`
**Description:** Creates a new medical record. The `file` field should contain a Base64-encoded string of the medical document (e.g., PDF, image).

**Request Body:**
```json
{
    "userId": 1,
    "name": "string",
    "type": "string",
    "date": "YYYY-MM-DD",
    "file": "Base64 string"
}
```

**Response Body:**
```json
{
    "message": "Medical record created successfully",
    "record_id": 1
}
```

---

### `GET /api/v1/medical_records/user/<user_id>`
**Description:** Retrieves all medical records for a specific user.

**Request Body:** None

**Response Body:**
```json
[
    {
        "id": 1,
        "userId": 1,
        "name": "string",
        "type": "string",
        "date": "YYYY-MM-DD",
        "fileType": "string",
        "fileUrl": "string (path to file)",
        "createdAt": "string (ISO 8601)"
    }
]
```

---

### `PATCH /api/v1/medical_records/<record_id>`
**Description:** Updates a specific medical record. Only include the fields you wish to update. The `file` field accepts a Base64-encoded string of the new document.

**Request Body:**
```json
{
    "name": "string",
    "type": "string",
    "date": "YYYY-MM-DD",
    "file": "Base64 string"
}
```

**Response Body:**
```json
{
    "message": "Medical record updated successfully"
}
```

---

### `DELETE /api/v1/medical_records/<record_id>`
**Description:** Deletes a specific medical record.

**Request Body:** None

**Response Body:**
```json
{
    "message": "Medical record deleted successfully"
}
```