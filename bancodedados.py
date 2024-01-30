from pinterest import app, database
from pinterest.models import Post, Usuario

with app.app_context():
    database.create_all()