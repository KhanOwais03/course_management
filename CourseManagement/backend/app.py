from flask import Flask
from student import student
from Courses import courses
from enrollments import enrollments
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(student)
app.register_blueprint(courses)
app.register_blueprint(enrollments)

if __name__ =='__main__':
    app.run(debug=True,port=5000)

