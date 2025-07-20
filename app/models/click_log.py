from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import relationship
from app.database.base import Base


class ClickLog(Base):
    """
    SQLAlchemy model for storing details of each URL click.
    Represents the 'click_logs' table in the database.
    """
    __tablename__ = "click_logs"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id", ondelete="CASCADE"), nullable=False)
    clicked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    referrer = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)

    # Relationship to the Url model
    url = relationship("Url", backref="click_logs", doc="The URL that was clicked.")

    def __repr__(self) -> str:
        return (
            f"<ClickLog(id={self.id}, url_id={self.url_id}, "
            f"clicked_at='{self.clicked_at}', referrer='{self.referrer[:50] if self.referrer else ''}')>"
        )
