from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flasgger import Swagger, swag_from
import os

# Initialize app
app = Flask(__name__)

# Swagger configuration
swagger = Swagger(app)

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize marshmallow
ma = Marshmallow(app)

# Task Class/Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, title, description):
        self.title = title
        self.description = description

# Task Schema
class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task

# Initialize schema
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Create a Task
@app.route('/task', methods=['POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Task created successfully',
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'description': {'type': 'string'}
                }
            }
        }
    ]
})
def add_task():
    title = request.json['title']
    description = request.json['description']

    new_task = Task(title, description)

    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)

# Get All Tasks
@app.route('/task', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of all tasks',
        }
    }
})
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

# Get Single Task
@app.route('/task/<id>', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A single task',
        }
    },
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ]
})
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

# Update a Task
@app.route('/task/<id>', methods=['PUT'])
@swag_from({
    'responses': {
        200: {
            'description': 'Task updated successfully',
        }
    },
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'description': {'type': 'string'}
                }
            }
        }
    ]
})
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()

    return task_schema.jsonify(task)

# Delete Task
@app.route('/task/<id>', methods=['DELETE'])
@swag_from({
    'responses': {
        200: {
            'description': 'Task deleted successfully',
        }
    },
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ]
})
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

# Run Server
if __name__ == '__main__':
    #Drop db if it exists
    # db.drop_all()

    # Create db if it does not exist
    if not os.path.exists(database_path):
        with app.app_context():
            db.create_all()

    app.run(host='0.0.0.0', port=5000, debug=True)
