from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base


class Url(Base):
    """
    SQLAlchemy model for storing shortened URLs.
    Represents the 'urls' table in the database.
    """
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String(12), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    clicks = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expired_at = Column(DateTime(timezone=True), nullable=True)
    max_clicks = Column(Integer, nullable=True)
    one_time_use = Column(Boolean, default=False, nullable=False)

    # Relationship to the User model, linking URLs to their creators.
    user = relationship("User", back_populates="urls", lazy="joined")

    def __repr__(self) -> str:
        """
        Provides a string representation of the Url object for debugging.
        """
        return (
            f"<Url(id={self.id}, "
            f"short_code='{self.short_code}', "
            f"original_url='{self.original_url[:50]}{'...' if len(self.original_url) > 50 else ''}', "
            f"clicks={self.clicks}, max_clicks={self.max_clicks}, "
            f"one_time_use={self.one_time_use})>"
        )
