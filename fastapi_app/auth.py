from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import status, Depends
from database import Session, ENGINE
from db_models import *
from schemas import *
from werkzeug import security
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
import django
import os
from passlib.hash import django_pbkdf2_sha256


a_router = APIRouter(prefix='/auth', tags=['auth'])
session = Session(bind=ENGINE)


@a_router.get('/')
async def hello():
    return {
        'message': 'Hello World api!'
    }


@a_router.get('/login')
async def login():
    return {
        'message': 'this is login page!'
    }


@a_router.post('/login')
async def login(user: LoginUser, Authenzetion: AuthJWT = Depends()):
    username = session.query(User).filter(User.username == user.username).first()
    if username is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User topilmadi')

    user_check = session.query(User).filter(User.username == user.username).first()

    if user_check and django_pbkdf2_sha256.verify(user.password, user_check.password):
        access_token = Authenzetion.create_access_token(subject=user_check.username)
        refresh_token = Authenzetion.create_refresh_token(subject=user_check.username)
        data = {
            "code": 200,
            "msg": "login successful",
            "user": {
                "username": user_check.username
            },
            "token": {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }
        return jsonable_encoder(data)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Malumotlar topilmadi')


@a_router.post('/register')
async def register(user: RegisterUser):
    username = session.query(User).filter(User.username == user.username).first()
    if username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bunday foydalanuvchi mavjud boshqa yarating')

    email = session.query(User).filter(User.email == user.email).first()

    if email or username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bunday foydalanuvchi royxatdan otgan')

    new_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=django_pbkdf2_sha256.hash(user.password),
        date_joined=user.date_joined

    )

    session.add(new_user)
    session.commit()
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail='succes')


@a_router.get('/logout')
async def logout():
    return {
        'message': 'logout page'
    }
