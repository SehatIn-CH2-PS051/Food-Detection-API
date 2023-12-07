# Use an official Python runtime as a parent image
FROM python:3.8-slim

#Author
LABEL authors="Sehatin Team"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get -y install python3 python3-pip && \
    pip3 install virtualenv && \
    virtualenv -p python3 venv && \
    source venv/bin/activate && \
    pip install -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8000", "food_detection_api:app"]
