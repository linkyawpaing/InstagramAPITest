# Third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Initialize Flask app
app = Flask(__name__)

# Database configurations
DATABASE_URL = 'mysql+mysqldb://admin:admin@database/photobook'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db = SQLAlchemy(app)

# Create engine and scoped session
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
db_session = scoped_session(Session)
