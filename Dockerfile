# Use the official Python image

FROM python:3.11-slim



# Set working directory

WORKDIR /flask-app



# Cpoying requirements.txt to the Docker Image

COPY requirements.txt requirements.txt



# Installing dependencies from requirements.txt in Docker Image

RUN pip install -r requirements.txt



# Copying all files from the current directory to the Docker Image

COPY . .



# Navigating to the Blueprint_app directory to run commands to create the database

WORKDIR /flask-app/Blueprint_app



# Running the command to create the database

RUN flask db init

RUN flask db migrate

RUN flask db upgrade



# Moving back to your main working directory

WORKDIR /flask-app



CMD ["python", "run.py"]