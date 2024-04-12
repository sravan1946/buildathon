from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

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
    ):
        self.sid = sid
        self.name = name
        self.email = email
        self.password = password
        self.created_at = datetime.datetime.now()
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
@app.route("/signup", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        DOB = request.form.get("DOB")
        grade = request.form.get("grade")
        gender = request.form.get("gender")
        phone_no = request.form.get("phone_no")
        sid = str(uuid.uuid4())