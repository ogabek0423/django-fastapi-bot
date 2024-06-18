from fastapi import APIRouter
from database import Session, ENGINE
from schemas import *
from db_models import *
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from django.contrib.auth.hashers import make_password, check_password


session = Session(bind=ENGINE)
tg_router = APIRouter(prefix="/tg", tags=["tg"])


@tg_router.get('/')
async def get_users():
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        users = session.query(TelegramUser).all()
        context = [
            {
                "id": data.id,
                "full_name": data.fullname,
                "chat_id": data.chat_id,
                "username": data.username,
                "joined": data.created_time,

            }
            for data in users
        ]

        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@tg_router.get('/{id}')
async def get_user(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        user = session.query(Telegramuser).filter(Telegramuser.id ==id).first()
        data = user
        context = [
            {
                "id": data.id,
                "full_name": data.fullname,
                "chat_id": data.chat_id,
                "username": data.username,
                "joined": data.created_time,
            }

        ]

        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@tg_router.post('/create')
async def create_user(tg_user: TelegramUserBase, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        user_check = session.query(TelegramUser).filter(Telegramuser.id == tg_user.id).first()
        if user_check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user is already registered")

        new_adr = User(
                username=tg_user.username,
                fullname=tg_user.fullname,
                chat_id=tg_user.chat_id,
                id=tg_user.id,
        )
        session.add(new_adr)
        session.commit()

        return HTTPException(status_code=status.HTTP_201_CREATED, detail="user has been added")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only admins can create new addresses")


@tg_router.put('/{id}')
async def update_address(id: int, user: TelegramUserBase, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        adr_check = session.query(Telegramuser).filter(Telegramuser.id == id).first()
        new_id_check = session.query(Telegramuser).filter(Telegramuser.id == user.id).first()
        username_check = session.query(Telegramuser).filter(Telegramuser.username == user.username).first()
        if adr_check:
            if username_check is None or adr_check.username == user.username:
                if new_id_check is None:
                    for key, value in user.dict().items():
                        setattr(adr_check, key, value)
                        session.commit()

                    data = {
                        "code": 200,
                        "message": "user updated"
                    }
                    return jsonable_encoder(data)
                elif new_id_check.id == adr_check.id:
                    for key, value in user.dict().items():
                        setattr(adr_check, key, value)
                        session.commit()

                    data = {
                        "code": 200,
                        "message": "user updated"
                    }
                    return jsonable_encoder(data)
                return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Berilgan id da malumot mavjud!")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="berilgan city id mavjud emas!")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malumot topilmadi")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Only admins can edit this address')


@tg_router.delete('/{id}')
async def delete_user(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        item = session.query(Telegramuser).filter(Telegramuser.id == id).first()
        if item:
            session.delete(item)
            session.commit()
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Deleted")

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Malumot topilmadi")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only admins can delete this address")
