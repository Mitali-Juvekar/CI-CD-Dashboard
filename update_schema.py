from models import Base
from db import engine

if __name__ == "__main__":
    Base.metadata.create_all(engine, checkfirst=True)
    print("Schema updated successfully!")