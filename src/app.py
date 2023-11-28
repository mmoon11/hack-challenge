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
    categories = []
    categories.append(Category(name="Project Team"))
    categories.append(Category(name="STEM"))
    categories.append(Category(name="Business"))
    categories.append(Category(name="GreekLife"))
    categories.append(Category(name="Arts"))
    categories.append(Category(name="Social"))
    categories.append(Category(name="Cultural"))
    categories.append(Category(name="Environmental"))
    for category in categories:  
        db.session.add(category)
        db.session.commit()

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

# GET all categories
@app.route("/api/categories/")
def get_categories():
    """
    Endpoint for getting all categories
    """
    categories = [t.serialize() for t in Category.query.all()]
    return success_response({"categories":categories})

# GET all applications (not in order yet)
@app.route("/api/applications/")
def get_applications():
    """
    Endpoint for getting all applications 
    """
    applications = [t.serialize() for t in Application.query.all()]
    return success_response({"applications":applications})



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

# DELETE an application by id
@app.route("/api/applications/<int:application_id>/", methods=["DELETE"])
def delete_app_by_id(application_id):
    """
    Endpoint for deleting application by its id
    """
    application = Application.query.filter_by(id=application_id).first()
    if application is None:
        return failure_response("Application not found")
    db.session.delete(application)
    db.session.commit()
    return success_response(application.serialize())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
