from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://mitalijuvekar:MiTuLi26%4002@localhost:5432/ci_metrics',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=60,
    pool_recycle=3600  # Recycle connections after an hour
)
Session = sessionmaker(bind=engine)