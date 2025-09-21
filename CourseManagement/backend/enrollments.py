import mysql.connector
from flask import Blueprint
import datetime
from flask import Flask,jsonify,request
from flask_cors import CORS
enrollments = Blueprint('enrollments',__name__)


CORS(enrollments)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "assignment_1")


mycursor = mydb.cursor()

@enrollments.route("/enrollments",methods=["GET"])
def getenrollments():
    return jsonify(getlist())
   
def getlist():
    mycursor.execute("select * from enrollments")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    return myresult
mycursor = mydb.cursor()

@enrollments.route("/enrollments", methods=["POST"])
def addenrollments():
    try:
      
        new_enrollment = request.get_json()        
        student_id = new_enrollment.get("student_id")
        course_id = new_enrollment.get("course_id")    
        enrollment_date = datetime.datetime.now()  
        if not student_id or not course_id or not enrollment_date :
            return jsonify({"error": "Missing student_id or course_id or enrollment_date"}), 400

        added_enrollments = addenrollment1(student_id, course_id,enrollment_date)
        return jsonify(added_enrollments), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def addenrollment1(student_id, course_id,enrollment_date):
    sql = "INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES (%s, %s, %s)"
    val = (student_id, course_id, enrollment_date)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted")
    return {"student_id": student_id, "course_id": course_id, "enrollment_date": enrollment_date}

@enrollments.route("/student/<name>",methods=["PATCH"])
def updstudent (name):
    updatesstudent (name)
    return jsonify({"message": f"{name} updated successfully"}), 201
    
def updatesstudent(name):
    sql = f"update student set  name = 'Nasrulla' where name ='{name}'"
    mycursor.execute (sql)
    mydb.commit()
    print(mycursor.rowcount,"Record updated")


@enrollments.route("/student/<name>",methods = ['DELETE'])
def course (name):
    sql = f"delete from course where name = '{name}'"
    mycursor.execute (sql)
    
    mydb.commit()
    print(mycursor.rowcount,"Record deleted")
    return jsonify({"message":"student deleted successfully"}),204

