from pymongo import MongoClient
from passlib.context import CryptContext
from bson import ObjectId
from flask import Flask, request, session, render_template

# Flask App boilerplate
website = Flask(__name__)
#  Used for session encryption (!DO NOT EXPOSE IN PRODUCTION!)
website.secret_key = '8FdncbLeEvXEugscSWikJg'

# Database connection boilerplate
creds = ""
with open("connectionString.txt", 'r') as cred_file:
    creds = cred_file.readline()
client = MongoClient(creds)
db = client.capstone_dev
users = db.users
passwords = db.passwords
posts = db.posts

# Password library boilerplate
pwd_context = CryptContext(schemes=["bcrypt"])


@website.route("/create_user", methods=["POST"])
def create_user():
    # Grab username and password to send to DB
    # TODO Perform input validation!
    # TODO Catch all invalid use cases (email already in system)
    if request.method == 'POST':
        user_id = ObjectId()
        pass_id = ObjectId()
        user_data = {
                '_id': user_id,
                'fname': request.form['fname'],
                'lname': request.form['lname'],
                'email': request.form['email'],
                }
        pass_data = {
                '_id': pass_id,
                'user_id': user_id,
                'email': request.form['email'],
                'pass_hash': pwd_context.hash(request.form['password']),
                }
        users.insert_one(user_data)
        passwords.insert_one(pass_data)
        return "Success"
    else:
        return "Failure"


@website.route("/login", methods=["POST"])
def authenticate():
    # Compare input password to stored password
    # TODO sessions
    if request.method == "POST":
        search_user = {
                "email": request.form["email"]
                }
        user_info = users.find_one(search_user)
        try:
            search_pass = {
                    "user_id": user_info.get("_id"),
                    }
            pass_info = passwords.find_one(search_pass)
            if pwd_context.verify(request.form["password"], pass_info.get("pass_hash")):
                session["username"] = user_info.get("username")
                session["name"] = user_info.get("fname")
                return render_template("index.html", name=session["name"])
            else:
                return render_template("index.html")
        except:
            return "<h1>Username not found</h1>" + render_template("index.html")
    else:
        return "Failure"


@website.route("/listings", methods=["GET", "POST"])
def listings():
    # GET request for getting listings
    # POST request for creating listings
    pass


"""
@website.route("/test.html")
def test_page():
    if session.get("name"):
        return render_template("test.html", name=session["name"])
    else:
        return render_template("test.html")


@website.route("/")
def entry():
    if session.get("name"):
        return render_template("index.html", name=session["name"])
    else:
        return render_template("index.html")
"""
