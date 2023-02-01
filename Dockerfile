# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages
RUN pip install -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED 1