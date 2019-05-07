# Using alpine Docker image
FROM python:3.7-alpine

# MAINTAINER is deprecated so use LABEL instead
LABEL Mohd Haider Ali 

# Using unbuffered python to optimise python execution
ENV PYTHONUNBUFFERED 1

# Copying req. file from local to the Container
COPY ./requirements.txt /requirements.txt

# Installing req in Container
RUN pip install -r /requirements.txt

# Creating app dir and copying all local app data to Container
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Adding user in Container to use the App so as to secure it from 
# Attackers
RUN adduser -D user
USER user

