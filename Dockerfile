# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app inside the container
WORKDIR /app

# Copy the requirements file and install the dependencies
# This leverages Docker's layer caching to speed up builds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project folder from your local machine to the container
COPY . .

# Expose port 5000, as defined in run.py, to the outside world
EXPOSE 5000

# Run the Flask application
CMD ["python", "run.py"]