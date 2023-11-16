from db import db
from flask import Flask
from db import Category
from db import Application
from flash import request
import json
from sqlalchemy import asc

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

# Unfinished but a way I found to return applications in order
@app.route("/api/applications/<int:category_id>/")
def get_apps_by_category(category_id):
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return failure_response("Category not found")
    applications = Application.query.filter_by(category_id=category.id).order_by(asc(Application.month), asc(Application.day), asc(Application.year))
    return success_response([t.serialize() for t in applications])

# ADD APPLICATION:
# @app.route("/api/applications/", methods=["POST"])
# POST an application

# Also unfinished (and we might want input for category to be a String instead of category_id) 
@app.route("/api/applications/", methods=["POST"])
def create_application():
    body = json.loads(request.data)
    category_id = body.get("category_id")
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return failure_response("Category not found")
    new_application = Application(title=body.get("title"), club_name=body.get("club_name"), 
                                  description=body.get("description"), app_link=body.get("app_link"), 
                                  club_link=body.get("club_link"), month=body.get("month"), day=body.get("day"), 
                                  year=body.get("year"), category_id=body.get("category_id"))
    db.session.add(new_application)
    db.session.commit()
    return success_response(new_application.serialize(), 201)

# DELETE APPLICATION (past due date):
# @app.route("/api/applications/<int:application_id>/", methods=["DELETE"])
# DELETE an application by id

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
