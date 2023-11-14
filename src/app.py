from db import db
from flask import Flask
from db import Category
from db import Application
from flash import request
import json

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

# FOR HOME PAGE:
# @app.route("/api/applications/")
# GET all applications
    # in this one we look through each one and see if deadline passed to call DELETE

# FOR FILTERING:
# @app.route("/api/applications/<int:category_id>/")
# GET all applications by category id
    # I have a feeling the iOS people would input the category string (not category_id)
        # so wondering if we should also have a GET for getting category name -> category id?
        # or replace category_id by a category string (so that the front end can access it that way)

# ADD APPLICATION:
# @app.route("/api/applications/", methods=["POST"])
# POST an application

# DELETE APPLICATION (past due date):
# @app.route("/api/applications/<int:application_id>/", methods=["DELETE"])
# DELETE an application by id

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
