import os
from flask import Flask, render_template, request, redirect, session # 1. Added session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super-secret-key-change-this' # 2. Add this for session security
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///todo.db')
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(20), default='Medium')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'Papous34*':
            session['logged_in'] = True
            return redirect('/')
        else:
            return "Wrong password! <a href='/login'>Try again</a>"
    
    return render_template('login.html') #new login.html file pointer

@app.route('/', methods=['GET', 'POST'])
def index():
    # 4. Add this check to every route you want to protect
    if not session.get('logged_in'):
        return redirect('/login')
        
    if request.method == 'POST':
        task_content = request.form.get('content')
        task_priority = request.form.get('priority')
        new_task = Task(content=task_content, priority=task_priority)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')

    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# ... keep your delete and update routes the same ...

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating your task"
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
