from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_pymongo import PyMongo
import bcrypt
import subprocess
import os

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://EyeSpyTestDB:EyeSpyTest123@test.msyeg.mongodb.net/?retryWrites=true&w=majority&appName=Test"
mongo = PyMongo(app)

@app.route('/test_db')
def test_db():
    try:
        mongo.db.command('serverStatus')
        return "Connected successfully to MongoDB!"
    except Exception as e:
        return f"Failed to connect to MongoDB. Error: {str(e)}"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'username': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        
        return 'Username already exists!'

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for('home'))

        return 'Invalid username/password combination'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/capture_faces', methods=['POST'])
def capture_faces():
    name = request.form['name']
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'face_rec', 'capture_faces.py')
    subprocess.run(['python', script_path, name])
    return jsonify({'status': 'Faces captured successfully'})

@app.route('/train_recognizer', methods=['POST'])
def train_recognizer():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'face_rec', 'train_recognizer.py')
    subprocess.run(['python', script_path])
    return jsonify({'status': 'Recognizer trained successfully'})

@app.route('/run_webcam', methods=['POST'])
def run_webcam():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'face_rec', 'webcam.py')
    subprocess.run(['python', script_path])
    return jsonify({'status': 'Webcam started successfully'})

if __name__ == '__main__':
    app.run(debug=True)