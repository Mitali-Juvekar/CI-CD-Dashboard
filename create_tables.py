from sqlalchemy import create_engine
from models import Base

engine = create_engine('postgresql://mitalijuvekar:MiTuLi26%4002@localhost:5432/ci_metrics')

# Create all tables defined in models.py
Base.metadata.create_all(engine)

print("Database tables created successfully!")