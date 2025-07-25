from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config import db


class Performance(db.Model):
    __tablename__ = 'performance'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    date = Column(Date, nullable=False)
    trips = Column(Integer, default=0)
    fare_collected = Column(Float, default=0.0)
    commission = Column(Float, default=0.0)
    route = Column(String(100))
    
    # Relationship with User model
    employee = relationship('User', backref='performances')

    def __repr__(self):
        return f"Performance(employee_id={self.employee_id}, date={self.date}, trips={self.trips}, fare_collected={self.fare_collected}, commission={self.commission}, route={self.route})"