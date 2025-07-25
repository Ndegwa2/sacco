from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Performance(Base):
    __tablename__ = 'performance'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    trips = Column(Integer)
    fare_collected = Column(Float)
    commission = Column(Float)
    route = Column(String)

    def __repr__(self):
        return f"Performance(date={self.date}, trips={self.trips}, fare_collected={self.fare_collected}, commission={self.commission}, route={self.route})"