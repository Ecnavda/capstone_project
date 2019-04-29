import os
from pymongo import MongoClient
from passlib.context import CryptContext
from bson import ObjectId
from flask import Flask, request, session, render_template, redirect

# Flask App boilerplate
website = Flask(__name__)
#  Used for session encryption (!DO NOT EXPOSE IN PRODUCTION!)
website.secret_key = '8FdncbLeEvXEugscSWikJg'
#  Location of pictures uploaded
upload_folder = "static/images/"
website.config["UPLOAD FOLDER"] = upload_folder

# Database connection boilerplate
creds = ""
with open("connectionString.txt", 'r') as cred_file:
    creds = cred_file.readline()
client = MongoClient(creds)
# Commented out the following as it isn't multiprocessor safe (won't work)
# Each function gets its own client as it triggers
"""
db = client.capstone_dev
users = db.users
passwords = db.passwords
posts = db.posts
"""

# Password library boilerplate
pwd_context = CryptContext(schemes=["bcrypt"])


@website.route("/listings_old")
def deleteme():
    if session.get("name"):
        return render_template("bx_listings_old.html", name=session.get("name"))
    else:
        return render_template("bx_listings_old.html")

@website.route("/create_user", methods=["GET", "POST"])
def create_user():
    db = MongoClient(creds).capstone_dev
    users = db.users
    passwords = db.passwords
    # posts = db.posts
    # Grab username and password to send to DB
    # TODO Perform input validation!
    # TODO Catch all invalid use cases (email already in system)
    if request.method == "POST":
        user_id = ObjectId()
        pass_id = ObjectId()
        user_data = {
                "_id": user_id,
                "fname": request.form["fname"],
                "lname": request.form["lname"],
                "email": request.form["username"],
                }
        pass_data = {
                '_id': pass_id,
                'user_id': user_id,
                'email': request.form["username"],
                'pass_hash': pwd_context.hash(request.form["password"]),
                }
        users.insert_one(user_data)
        passwords.insert_one(pass_data)
        session["username"] = request.form["username"]
        session["name"] = request.form["fname"]
        return render_template("bx_index.html", name=session["name"])
    elif request.method == "GET":
        return render_template("bx_create_user.html")


@website.route("/create_listing", methods=["GET"])
def create_listing():
    if session.get("name"):
        return render_template("bx_create_listing.html", name=session.get("name"))
    else:
        return render_template("bx_create_listing.html")


@website.route("/login", methods=["GET", "POST"])
def authenticate():
    db = MongoClient(creds).capstone_dev
    users = db.users
    passwords = db.passwords
    # posts = db.posts
    # Compare input password to stored password
    # TODO sessions
    if request.method == "POST":
        search_user = {
                "email": request.form["username"]
                }
        user_info = users.find_one(search_user)
        try:
            search_pass = {
                    "user_id": user_info.get("_id"),
                    }
            pass_info = passwords.find_one(search_pass)
            if pwd_context.verify(request.form["password"], pass_info.get("pass_hash")):
                session["username"] = user_info.get("email")
                session["name"] = user_info.get("fname")
                return render_template("bx_index.html", name=session["name"])
            else:
                return render_template("index.html")
        except:
            return "<h1>Username not found</h1>" + render_template("bx_index.html")
    elif request.method == "GET":
        return render_template("bx_login.html")


@website.route("/listings", methods=["GET", "POST"])
def listings():
    db = MongoClient(creds).capstone_dev
    # GET request for getting listings
    if request.method == "GET":
        all_posts = db.posts.find()

        if session.get("name"):
            return render_template("bx_listings.html", name=session.get("name"), postings=all_posts)
        else:
            return render_template("bx_listings.html", postings=all_posts)

    # POST request for creating listings
    elif request.method == "POST":
        if session.get("name"):
            user = db.users.find_one({"email": session.get("username")})
            posts = db.posts
            picture_file = request.files["picture"]
            data = {
                    "userid": user.get("_id"),
                    "item": request.form["item"],
                    "description": request.form["description"],
                    "price": request.form["price"],
                    "location": request.form["location"],
                    "picture": picture_file.filename,
                    }
            posts.insert_one(data)
            picture_file.save(os.path.join(website.config["UPLOAD FOLDER"], picture_file.filename))
            all_posts = posts.find()

            return render_template("bx_listings.html", name=session.get("name"), postings=all_posts)
        # check if logged in first
        # send info to database and  return listings
    else:
        return "Log in"


@website.route("/", methods=["GET", "POST"])
def back_index():
    if session.get("name"):
        print(session)
        return render_template("bx_index.html", name=session.get("name"))
    else:
        return render_template("bx_index.html")


@website.route("/about", methods=["GET", "POST"])
def back_about():
    if session.get("name"):
        return render_template("bx_about.html", name=session.get("name"))
    else:
        return render_template("bx_about.html")


@website.route("/contact", methods=["GET", "POST"])
def back_contact():
    if session.get("name"):
        return render_template("bx_contact.html", name=session.get("name"))
    else:
        return render_template("bx_contact.html")


@website.route("/logout")
def logout():
    session.clear()
    return render_template("bx_index.html")
