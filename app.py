from pymongo import MongoClient
from flask import Flask
website = Flask(__name__)


# Database connection boilerplate
creds = ""
with open("connectionString.txt", 'r') as cred_file:
    creds = cred_file.readline()
client = MongoClient(creds)
db = client.capstone_dev
users = db.users
passwords = db.passwords
posts = db.posts


@website.route("/create_user", methods=["POST"])
def create_user():
    pass


@website.route("/auth", methods=["POST"])
def authenticate():
    pass


@website.route("/listings", methods=["GET", "POST"])
def listings():
    # GET request for getting listings
    # POST request for creating listings
    pass