import mysql.connector
from flask import Blueprint
from flask import Flask,jsonify,request
from flask_cors import CORS
student = Blueprint('student',__name__)


CORS(student)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "assignment_1")

mycursor = mydb.cursor()

@student.route("/student",methods=["GET"])
def getStudent():
    return jsonify(getStudentList())

@student.route("/login",methods = ["POST"])
def loginuser():
    try:
        creds = request.get_json()
        username = creds["username"]
        password = creds["password"]
        
        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        authenticated_user = authuser(username, password)
        return jsonify(authenticated_user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def authuser(username,password):
    query = f"select * from student where username = '{username}' and password = '{password}'"
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    return myresult


@student.route("/login", methods=["OPTIONS"])
def login_options():
    return {}, 200

def getStudentList():
    mycursor.execute("select * from student")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    return myresult
mycursorycursor = mydb.cursor()

@student.route("/student", methods=["POST"])
def addstudent():
    try:
      
        new_student = request.get_json()        
        name = new_student.get("name")
        email = new_student.get("email")        
        if not name or not email:
            return jsonify({"error": "Missing name or email"}), 400

        added_student = addstudent1(name, email)
        return jsonify(added_student), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def addstudent1(name, email):
    sql = "INSERT INTO student (name, email) VALUES (%s, %s)"
    val = (name, email)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted")
    return {"name": name, "email": email}

@student.route("/student/<name>",methods=["PATCH"])
def updstudent (name):
    updatesstudent (name)
    return jsonify({"message": f"{name} updated successfully"}), 201
    
def updatesstudent(name):
    sql = f"update student set  name = 'Nasrulla' where name ='{name}'"
    mycursor.execute (sql)
    mydb.commit()
    print(mycursor.rowcount,"Record updated")


@student.route("/student/<name>",methods = ['DELETE'])
def deleteStudent (name):
    sql = f"delete from course where name = '{name}'"
    mycursor.execute (sql)
    
    mydb.commit()
    print(mycursor.rowcount,"Record deleted")
    return jsonify({"message":"student deleted successfully"}),204
