from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random
from models import Base, Build, TestResult

# EXPLICITLY specify the database connection details
engine = create_engine('postgresql://mitalijuvekar:MiTuLi26%4002@localhost:5432/ci_metrics', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Insert a single build to test
    build = Build(
        timestamp=datetime.now(),
        duration=150,
        status="success",
        test_results="Script test"
    )
    
    session.add(build)
    session.commit()
    
    # Query to verify
    count = session.query(Build).count()
    print(f"Current build count: {count}")
    
    # Add more builds if the first one worked
    if count > 0:
        for i in range(9):  # Add 9 more for a total of 10
            timestamp = datetime.now() - timedelta(days=i+1)
            build = Build(
                timestamp=timestamp,
                duration=random.randint(60, 300),
                status=random.choice(["success", "failure", "aborted"]),
                test_results=random.choice(["all passed", "some failed", "all failed"])
            )
            session.add(build)
        
        session.commit()
        print(f"Final build count: {session.query(Build).count()}")
        
except Exception as e:
    session.rollback()
    print(f"Error: {e}")
finally:
    session.close()