
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class EmailConfiguration(Base):
    __tablename__ = "email_configurations"

    id = Column(Integer, primary_key=True, index=True)


    smtp_user = Column(String, nullable=False)
    smtp_password = Column(String, nullable=False)
