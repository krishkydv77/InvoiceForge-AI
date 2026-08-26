from sqlalchemy import Column, Integer, String, Float, Date, Text
from database import Base

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String(50), unique=True, index=True)
    customer_name = Column(String(100))
    mobile = Column(String(20))
    address = Column(Text)
    items = Column(Text)   # JSON string
    total = Column(Float)
    tax = Column(Float)
    due_date = Column(Date)
    status = Column(String(20), default="generated")
