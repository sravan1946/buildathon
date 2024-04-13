from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import json
import datetime
import uuid
import os


class Student(UserMixin):
    def __init__(
        self,
        sid,
        name,
        email,
        password,
        DOB,
        grade,
        gender,
        phone_no,
        **kwargs
    ):
        self.sid = sid
        self.name = name
        self.email = email
        self.password = password
        self.created_at = datetime.datetime.now().timestamp()
        self.DOB = DOB
        self.grade = grade
        self.gender = gender
        self.phone_no = phone_no

    def get_id(self):
        return self.sid

    def to_dict(self):
        return {
            "sid": self.sid,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "DOB": self.DOB,
            "grade": self.grade,
            "gender": self.gender,
            "phone_no": self.phone_no,
        }

    def __repr__(self):
        return f"Student(sid={self.sid}, name={self.name}, email={self.email}, password={self.password}, created_at={self.created_at}, DOB={self.DOB}, grade={self.grade}, gender={self.gender}, phone_no={self.phone_no})"

    def __dict__(self):
        return self.to_dict()

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(sid):
    with open("./data/students.json", "r") as f:
        students = json.load(f)
    for student in students:
        if student["sid"] == sid:
            return Student(**student)
    return None

@app.route("/register", methods=["POST", "GET"])
@app.route("/register/", methods=["POST", "GET"])
@app.route("/signup", methods=["POST", "GET"]) # type: ignore
def register():
    if current_user.is_authenticated:
        return redirect(url_for("student_dashboard"))
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        print(request.form)
        DOB: str = datetime.date(*map(int, request.form.get("DOB").split("-"))).isoformat()
        grade = request.form.get("grade")
        gender: str = request.form.get("gender", "male")
        phone_no: int = request.form.get("phone_no", 0, type=int)
        sid: int = int(str(uuid.uuid4().int)[:14])
        student = Student(
            sid=sid,
            name=name,
            email=email,
            password=password,
            DOB=DOB,
            grade=grade,
            gender=gender,
            phone_no=phone_no,
        )
        try:
            with open("./data/students.json", "r") as f:
                students = json.load(f)
        except FileNotFoundError:
            with open("./data/students.json", "w") as f:
                json.dump([], f)
            students = []
        if student.email in [student["email"] for student in students]:
            return render_template("register.html", error="Email already exists")
        if student.phone_no in [student["phone_no"] for student in students]:
            return render_template("register.html", error="Phone Number already exists")
        if student.DOB > datetime.date.today().isoformat():
            return render_template("register.html", error="Invalid Date of Birth")
        students.append(student.to_dict())
        with open("./data/students.json", "w") as f:
            json.dump(students, f, default=lambda x: x.__dict__())
        return redirect(url_for("login", error="Registration Successful. Please login to continue"))
    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
@app.route("/login/", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        with open("./data/students.json", "r") as f:
            students = json.load(f)
        for student in students:
            if student["email"] == email and student["password"] == password:
                student = Student(**student)
                login_user(student, force=True)
                session["student"] = student.to_dict()
                session["logged_in"] = True
                return redirect(url_for("dashboard"))
        return redirect(url_for("login", error="Invalid Credentials"))
    return render_template("login.html")

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")