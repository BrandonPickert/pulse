from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workouts = relationship('Workout', back_populates='user', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Workout(Base):
    __tablename__ = 'workouts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    username = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    duration = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='workouts')
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'type': self.type,
            'duration': self.duration,
            'notes': self.notes,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
