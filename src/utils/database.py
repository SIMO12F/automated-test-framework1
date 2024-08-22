from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import Config
from src.logger import logger

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

# Create the database engine
engine = create_engine(Config.DATABASE_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

def setup_database():
    """Create the database tables."""
    try:
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

def teardown_database():
    """Drop the database tables."""
    try:
        Base.metadata.drop_all(engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping database tables: {str(e)}")
        raise

def add_user(name, email):
    """Add a new user to the database."""
    session = Session()
    try:
        new_user = User(name=name, email=email)
        session.add(new_user)
        session.commit()
        logger.info(f"User added successfully: {name} ({email})")
        return new_user.id
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding user: {str(e)}")
        raise
    finally:
        session.close()

def get_user(user_id):
    """Get a user by ID."""
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            logger.info(f"User retrieved: {user.name} ({user.email})")
        else:
            logger.warning(f"User not found with ID: {user_id}")
        return user
    except Exception as e:
        logger.error(f"Error retrieving user: {str(e)}")
        raise
    finally:
        session.close()