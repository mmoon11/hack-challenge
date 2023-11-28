from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    """
    Categories Model
    """
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    applications = db.relationship("Application")

    def __init__(self, **kwargs):
        """
        Initialize a Category object
        """
        self.name = kwargs.get("name", "")

    def serialize(self):
        """
        Serialize a Category object
        """
        return {
            "id": self.id,
            "name": self.name
        }
    
class Application(db.Model):
    """
    Application Model
    """
    __tablename__ = "application"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    club_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    app_link = db.Column(db.String, nullable=False)
    club_link = db.Column(db.String)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize an Application object
        """
        self.title = kwargs.get("title", "")
        self.club_name = kwargs.get("club_name", "")
        self.description = kwargs.get("description", "")
        self.app_link = kwargs.get("app_link", "")
        self.club_link = kwargs.get("club_link", "")
        self.month = kwargs.get("month", 0)
        self.day = kwargs.get("day", 0)
        self.year = kwargs.get("year", 0)
        self.hour = kwargs.get("hour", 0)
        self.minute = kwargs.get("minute", 0)
        self.category_id = kwargs.get("category_id", 0)
    
    def serialize(self):
        """
        Serialize an Application object
        """
        category = Category.query.filter_by(id=self.category_id).first()
        return {
            "id": self.id,
            "title": self.title,
            "club_name": self.club_name,
            "description": self.description,
            "app_link": self.app_link,
            "club_link": self.club_link,
            "month": self.month,
            "day": self.day,
            "year": self.year,
            "hour": self.hour,
            "minute": self.minute,
            "category": category.serialize()
        }
