from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Build(Base):
    __tablename__ = 'builds'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    duration = Column(Integer)
    status = Column(String)
    test_results = Column(String)
    branch = Column(String)
    commit_hash = Column(String)  

class TestResult(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True)
    build_id = Column(Integer, nullable=False)  # Foreign Key reference to Build
    test_name = Column(String(50), nullable=False)
    result = Column(String(20))
    execution_time = Column(Integer)
