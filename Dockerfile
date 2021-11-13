# syntax=docker/dockerfile:1

# Dockerfile is a standardized way for Docker to build Docker Image.

# We need to say to Docker what base image we would like to use for our application.
FROM python:3

# The environment variable ensures that the the python output is
# set straight to the terminal without buffering it first
ENV PYTHONUNBUFFERED=1

# Set working directory to /TaskLab
WORKDIR /TaskLab

# Copy the current directory contents into the container at /TaskLab
COPY requirements.txt /TaskLab/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY . /TaskLab/