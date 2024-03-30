from fastapi import FastAPI
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware

from routers import auth
from db import engine, session

app = FastAPI()

app = FastAPI()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app.include_router(auth.router)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="mysecretkey", session_cookie="login_session")

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = session
    response = await call_next(request)
    request.state.db.close()
    return response
