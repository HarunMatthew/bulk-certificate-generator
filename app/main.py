from fastapi import FastAPI

from app.database import Base, engine
from app.api.routes import router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Bulk Certificate Generator API", version="1.0.0")


# Register API routes
app.include_router(router)


@app.get("/")
def root():
    return {"message": "Bulk Certificate Generator API is running"}
