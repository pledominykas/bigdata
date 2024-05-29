# Big Data task 2

## Description

This project is a simple CRUD To Do application built with Flask, SQLite, and Swagger.

## How to run the app (container registry)

1. Pull the Docker image from Docker Hub:

   ```sh
   docker pull pledominykas/flask-todo-app:latest
   ```

2. Run the Docker container:
   ```sh
   docker run -p 5000:5000 pledominykas/flask-todo-app:latest
   ```

## How to run the app (manual)

1. Build the Docker image:

   ```sh
   docker build -t flask-todo-app .
   ```

2. Run the Docker container:

   ```sh
   docker run --name BigData2FlaskToDo -p 5000:5000 flask-todo-app
   ```

## How to use the app:

1. Access the Swagger UI:
   Open your web browser and navigate to `http://localhost:5000/apidocs` to interact with the API.

2. You can click 'Try it out' on each endpoint and perform requests that will create, read, update or delete todo tasks in the SQLLite database through the Flask API.
