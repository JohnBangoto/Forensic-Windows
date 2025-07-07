# backend/app/models.py
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text, Boolean
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # modifié ici
    created_at = Column(DateTime, default=func.now())

    sessions = relationship("CollectionSession", back_populates="user", cascade="all, delete")

class CollectionSession(Base):
    __tablename__ = "collection_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hostname = Column(String(255), nullable=False)
    system = Column(String(100))
    collection_date = Column(DateTime, default=func.now())
    file_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    uploaded_to_drive = Column(Boolean, default=False)
    drive_url = Column(Text)
    error_count = Column(Integer, default=0)

    user = relationship("User", back_populates="sessions")
