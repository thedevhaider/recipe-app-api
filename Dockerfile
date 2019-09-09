# Using alpine Docker image
FROM python:3.7-alpine

# MAINTAINER is deprecated so use LABEL instead
LABEL Mohd Haider Ali

# Using unbuffered python to not buffer the ouput before printing
ENV PYTHONUNBUFFERED 1

# Copying req. file from local to the Container
COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client jpeg-dev

# Installing dependencies for psycopg2 (Postgres client)
# Set the alias using --virtual to delete the dependencies after use. 
# .tmp-build-dps is the alias to del dependecies
RUN apk add --update --no-cache --virtual .tmp-build-dps \ 
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

# Installing req in Container
RUN pip install -r /requirements.txt

# Removing Postgres client dependencies
RUN apk del .tmp-build-dps

# Creating app dir and copying all local app data to Container
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Create media folder to store image files
RUN mkdir -p /vol/web/media

# Create static folder to store html/css/js files
RUN mkdir -p /vol/web/static

# Adding user in Container to use the App so as to secure it from
# Attackers
RUN adduser -D user

# Giving app user permission to access /vol/ directory
RUN chown -R user:user /vol/

# Setting permissions of /vol/web
RUN chmod -R 755 /vol/web

# Setting user as the app user
USER user
