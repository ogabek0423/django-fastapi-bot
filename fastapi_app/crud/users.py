from fastapi import APIRouter
from database import Session, ENGINE
from schemas import *
from db_models import *
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from passlib.hash import django_pbkdf2_sha256


session = Session(bind=ENGINE)
user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get('/')
async def get_users(Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        users = session.query(User).all()
        context = [
            {
                "id": data.id,
                "first_name": data.first_name,
                "last_name": data.last_name,
                "username": data.username,
                "email": data.email,

            }
            for data in users
        ]

        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@user_router.get('/{id}')
async def get_user(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        user = session.query(User).filter(User.id ==id).first()
        data = user
        context = [
            {
                "id": data.id,
                "first_name": data.first_name,
                "last_name": data.last_name,
                "username": data.username,
                "email": data.email,
            }

        ]

        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@user_router.post('/create')
async def create_user(user: UserBase, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        user_check = session.query(User).filter(User.id == user.id).first()
        if user_check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user is already registered")

        new_adr = User(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            password=django_pbkdf2_sha256.hash(user.password)
        )
        session.add(new_adr)
        session.commit()

        return HTTPException(status_code=status.HTTP_201_CREATED, detail="user has been added")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only admins can create new addresses")


@user_router.put('/{id}')
async def update(id: int, user: UserBase, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        adr_check = session.query(User).filter(User.id == id).first()
        new_id_check = session.query(User).filter(User.id == user.id).first()
        username_check = session.query(User).filter(User.username == user.username).first()
        if adr_check:
            if username_check:
                if new_id_check is None:
                    for key, value in user.dict().items():
                        user.__dict__["password"] = django_pbkdf2_sha256.hash(user.password)
                        setattr(adr_check, key, value)
                        session.commit()

                    data = {
                        "code": 200,
                        "message": "user updated"
                    }
                    return jsonable_encoder(data)
                elif new_id_check.id == adr_check.id:
                    for key, value in user.dict().items():
                        user.__dict__["password"] = django_pbkdf2_sha256.hash(user.password)
                        setattr(adr_check, key, value)
                        session.commit()

                    data = {
                        "code": 200,
                        "message": "user updated"
                    }
                    return jsonable_encoder(data)
                return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Berilgan id da malumot mavjud!")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="berilgan username mavjud !")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malumot topilmadi")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Only admins can edit this address')


@user_router.delete('/{id}')
async def delete_user(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        item = session.query(User).filter(User.id == id).first()
        if item:
            session.delete(item)
            session.commit()
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Deleted")

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Malumot topilmadi")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only admins can delete this ")
