from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.database.base import Base


class User(Base):
    """
    SQLAlchemy model for storing user accounts.
    Represents the 'users' table in the database.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationship to the Url model, linking users to their shortened URLs.
    urls = relationship("Url", back_populates="user")

    def __repr__(self) -> str:
        """
        Provides a string representation of the User object for debugging.
        """
        return f"<User(id={self.id}, email='{self.email}')>"
