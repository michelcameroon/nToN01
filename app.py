from flask import Flask, render_template, request, redirect, url_for
from models import db, Student, Course

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#@app.before_first_request
@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('index.html', students=students, courses=courses)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    new_student = Student(name=name)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_course', methods=['POST'])
def add_course():
    name = request.form.get('name')
    new_course = Course(name=name)
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/enroll_student', methods=['POST'])
def enroll_student():
    student_id = request.form.get('student_id')
    course_id = request.form.get('course_id')
    student = Student.query.get(student_id)
    course = Course.query.get(course_id)
    if student and course:
        student.courses.append(course)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
