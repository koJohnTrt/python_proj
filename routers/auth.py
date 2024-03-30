from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.sessions import SessionMiddleware

from db import SessionLocal
from utils.db_utils import get_db

from models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username, User.password == password).first()
    if user:
        # Store user information in session
        request.session['user_id'] = user.id
        request.session['username'] = user.username

        return templates.TemplateResponse("success.html", {"request": request, "username": request.session.get("username")})
    else:
        return templates.TemplateResponse("failure.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("failure.html", {"request": request})

    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    if user:
        request.session['username'] = user.username
        return templates.TemplateResponse("success.html", {"request": request, "username": request.session.get("username")})
    else:
        return templates.TemplateResponse("failure.html", {"request": request})
