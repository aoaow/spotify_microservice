# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask/Gunicorn will run on
EXPOSE 5000

# Use gunicorn as the production server
CMD ["gunicorn", "--workers=4", "--threads=2", "-b", "0.0.0.0:5000", "app:app"]
