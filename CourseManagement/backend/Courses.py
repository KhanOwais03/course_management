import mysql.connector
from flask import Blueprint
from flask import Flask, jsonify, request
from flask_cors import CORS

courses = Blueprint('courses',__name__)

CORS(courses)

def getconn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="assignment_1"
    )

mycursor = getconn().cursor(dictionary=True)  


@courses.route("/courses", methods=["GET"])
def getcourses():
    mydb = getconn()
    with mydb.cursor(dictionary=True) as mycursor:
        mycursor.execute("SELECT * FROM courses")
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return jsonify(myresult)  

@courses.route("/enrolledcourses/<student_id>", methods=["GET"])
def getEnrolledcourses(student_id):
    mydb = getconn()
    with mydb.cursor(dictionary=True) as mycursor:
        mycursor.execute("SELECT distinct(id), c.title, c.description from assignment_1.courses c inner join assignment_1.enrollments e on c.c_id = e.course_id where student_id = 1") # + student_id)
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return jsonify(myresult)  

@courses.route("/othercourses/<student_id>", methods=["GET"])
def getOthercourses(student_id):
    mydb = getconn()
    with mydb.cursor(dictionary=True) as mycursor:
    #    mycursor.execute("SELECT distinct(id), c.title, c.description from assignment_1.courses c inner join assignment_1.enrollments e on c.c_id != e.course_id where student_id =1") # + student_id)
        mycursor.execute("select * from courses") # + student_id)
     
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return jsonify(myresult)  

@courses.route("/courses", methods=["POST"])
def addcourse():
    try:
        new_course = request.get_json()
        title = new_course.get("title")
        description = new_course.get("description")

        if not title or not description:
            return jsonify({"error": "Missing title or description"}), 400

        added_course = addcourse1(title, description)
        return jsonify(added_course), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def addcourse1(title, description):
    sql = "INSERT INTO courses (title, description) VALUES (%s, %s)"
    val = (title, description)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"id": mycursor.lastrowid, "title": title, "description": description}


@courses.route("/course/<title>", methods=["PATCH"])
def updCourse(title):
    updatescourses(title)
    return jsonify({"message": f"{title} updated successfully"}), 200


def updatescourses(title):
    sql = "UPDATE courses SET title = 'Introduction to Python Programming' WHERE title = %s"
    mycursor.execute(sql, (title,))
    mydb.commit()


@courses.route("/course/<title>", methods=['DELETE'])
def course(title):
    sql = "DELETE FROM courses WHERE title = %s"
    mycursor.execute(sql, (title,))
    mydb.commit()
    return jsonify({"message": "course deleted successfully"}), 200


