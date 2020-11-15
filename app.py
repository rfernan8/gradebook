from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DATABASE_URI
import sys

app = Flask(__name__) 
# config the SQLAlchemy connection to the database as your own database
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

migrate = Migrate(app, db)

# TODO: Edit these classes (and add others) to represent entities in our ER diagram
class student(db.Model):
    __tablename__ = 'student' # specify the table name if it is different from class name
    sid = db.Column(db.Integer, primary_key=True) # define ID 
    first_name = db.Column(db.String(), nullable=False) # define description
    last_name = db.Column(db.String(), nullable=False, default=False)
    
class teacher(db.Model):
    __tablename__ = 'teacher'
    tid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    
class parent(db.Model):
    __tablename__ = 'parent'
    pid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False) 
    
class teaches(db.Model):
    __tablename__ = 'teaches'
    tid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, primary_key=True)    
    
 class enrolled(db.Model):
    __tablename__ = 'enrolled'
    sid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, primary_key=True)    
    
 class assignment(db.Model):
    __tablename__ = 'enrolled'
    cid = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.Integer, primary_key=True)    
    letter = db.Column(db.String(), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    
 class class(db.Model):
    __tablename__ = 'class'
    cid = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(), nullable=False)
 
class category(db.Model):
    __tablename__ = 'category'
    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), primary_key=True)    
    weight = db.Column(db.Weight, nullable=False)
    
    
# TODO: Edit these functions to match the intended functionality of our database
#db.create_all() # create database based on class definition
@app.route("/")
def welcome():
    return render_template("home.html")

@app.route('/todos/create', methods=['POST'])
def create_todo():
    # description = request.form.get('description')
    # if not description:
    #     description = 'Do Nothing'
    # todo = Todo(description = description)
    # db.session.add(todo)
    # db.session.commit()
    # return redirect(url_for('index'))
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        if not description:
            description = 'Do Nothing'
        todo = Todo(description = description, completed=False, list_id=list_id)
        body['description'] = todo.description
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['completed'] = todo.completed
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)
        #      return jsonify({
        #     'description': todo.description
        # })

@app.route('/todos/<todo_id>/delete', methods=['DELETE'])
def delete_todo(todo_id):
    error = False
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify({'success': True})

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    error = False
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return '', 200

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

@app.route('/lists/<list_id>') # tell Flask what URL should trigger the function
# the function is given a name which is used to generate URLs for that particular function and returns the message we want to display in browser, function name does not matter
def get_list_todos(list_id):
    lists = TodoList.query.all()
    active_list = TodoList.query.get(list_id)
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()
    
    return render_template('index.html',todos=todos, lists=lists, active_list=active_list)

@app.route('/lists/create', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        if not name:
            name = 'Causal'
        todolist = TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['id'] = todolist.id
        body['name'] = todolist.name
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)



@app.route('/lists/<list_id>/delete', methods=['DELETE'])
def delete_list(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        for todo in list.todos:
            db.session.delete(todo)
        
        db.session.delete(list)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify({'success': True})

@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def set_completed_list(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        set_completed = request.get_json()['set_completed']

        for todo in list.todos:
            todo.completed = set_completed
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return '', 200

