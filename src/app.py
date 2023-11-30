from db import db
from flask import Flask
from db import Category
from db import Application
from flask import request
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
    if not Category.query.first():
        categories = []
        categories.append(Category(name="project-team"))
        categories.append(Category(name="stem"))
        categories.append(Category(name="business"))
        categories.append(Category(name="greek-life"))
        categories.append(Category(name="arts"))
        categories.append(Category(name="social"))
        categories.append(Category(name="cultural"))
        categories.append(Category(name="environmental"))
        for category in categories:  
            db.session.add(category)
        db.session.commit()

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

@app.route("/api/categories/")
def get_categories():
    """
    Endpoint for getting all categories
    """
    categories = [t.serialize() for t in Category.query.all()]
    return success_response({"categories":categories})

@app.route("/api/applications/")
def get_applications():
    """
    Endpoint for getting all applications 
    """
    applications = [t.serialize() for t in Application.query.order_by(asc(Application.year), asc(Application.month), asc(Application.day), asc(Application.hour),asc(Application.minute))]
    return success_response({"applications":applications})

@app.route("/api/applications/<string:category>/")
def get_apps_by_category(category):
    """
    Endpoint for getting applications by category
    """
    category_id = Category.query.filter_by(name=category).first().id
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return failure_response("Category not found")
    applications = Application.query.filter_by(category_id=category.id).order_by(asc(Application.year), asc(Application.month), asc(Application.day),asc(Application.hour),asc(Application.minute))
    return success_response([t.serialize() for t in applications])

@app.route("/api/applications/", methods=["POST"])
def create_application():
    """
    Endpoint for creating an application
    """
    body = json.loads(request.data)
    category = body.get("category")
    category_id = Category.query.filter_by(name=category).first().id

    if category_id is None:
        return failure_response("Category not found")
    if (body.get("title") is None) or (body.get("club_name") is None) or (body.get("description") is None) or (body.get("app_link") is None) or (body.get("club_link") is None) or (body.get("image_link") is None) or (body.get("second_image_link") is None) or (body.get("chat_link") is None) or (body.get("month") is None) or (body.get("day") is None) or (body.get("year") is None) or (body.get("hour") is None) or (body.get("minute") is None):
        return failure_response("Missing argument",400)
    new_application = Application(title=body.get("title"), club_name=body.get("club_name"), 
                                  description=body.get("description"), app_link=body.get("app_link"), 
                                  club_link=body.get("club_link"), image_link=body.get("image_link"), second_image_link=body.get("second_image_link"), chat_link=body.get("chat_link"), month=body.get("month"), day=body.get("day"), 
                                  year=body.get("year"), hour=body.get("hour"), minute=body.get("minute"), category_id=category_id)
    db.session.add(new_application)
    db.session.commit()
    return success_response(new_application.serialize(), 201)

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
