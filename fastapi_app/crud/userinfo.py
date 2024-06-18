from fastapi import APIRouter
from database import Session, ENGINE
from schemas import *
from db_models import *
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from django.contrib.auth.hashers import make_password, check_password


session = Session(bind=ENGINE)
user_info_router = APIRouter(prefix="/user_info", tags=["user_info"])


@user_info_router.get('/')
async def get_users():
    # try:
    #     Authentiztion.jwt_required()
    #
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')
    #
    # check_user_token = Authentiztion.get_jwt_subject()
    # check_user = session.query(User).filter(User.username == check_user_token).first()
    # if check_user.is_active:
    users = session.query(UserInfo).all()
    context = [
        {
            "id": data.id,
            "user":{
                "first_name": data.user.first_name,
                "last_name": data.user.last_name,
                "username": data.user.username,
                "email": data.user.email,
            },
            "photo": data.your_photo,
            "city": data.city,
            "street": data.street,
            "home_number": data.home_number,
            "user_number": data.user_number,
            "updated": data.last_update

        }
        for data in users
    ]

    return jsonable_encoder(context)
# return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@user_info_router.get('/{id}')
async def get_user(id: int, Authentiztion: AuthJWT = Depends()):
    # try:
    #     Authentiztion.jwt_required()
    #
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')
    #
    # check_user_token = Authentiztion.get_jwt_subject()
    # check_user = session.query(User).filter(User.username == check_user_token).first()
    # if check_user.is_active:
    user = session.query(UserInfo).filter(UserInfo.id ==id).first()
    data = user
    context = [
        {
            "id": data.id,
            "user":{
                "first_name": data.user.first_name,
                "last_name": data.user.last_name,
                "username": data.user.username,
                "email": data.user.email,
            },
            "photo": data.your_photo,
            "city": data.city,
            "street": data.street,
            "home_number": data.home_number,
            "user_number": data.user_number,
            "updated": data.last_update
        }

    ]

    return jsonable_encoder(context)
    # return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@user_info_router.post('/create')
async def create_user(user: UserInfoBase, Authentiztion: AuthJWT = Depends()):
    # try:
    #     Authentiztion.jwt_required()
    #
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')
    #
    # check_user_token = Authentiztion.get_jwt_subject()
    # check_user = session.query(User).filter(User.username == check_user_token).first()
    # if check_user.is_superuser:
    user_check = session.query(UserInfo).filter(UserInfo.id == user.id).first()
    user_auth = session.query(User).filter(User.id == user.user_id)
    if user_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user is already registered")
    if user_auth:
        new_adr = UserInfo(
            id=user.id,
            your_photo=user.your_photo,
            city=user.city,
            street=user.street,
            home_number=user.home_number,
            user_number=user.user_number,
            user_id=user.user_id

        )
        session.add(new_adr)
        session.commit()

        return HTTPException(status_code=status.HTTP_201_CREATED, detail="user has been added")
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")
    # return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only admins can create new addresses")


@user_info_router.put('/{id}')
async def update(id: int, user: UserInfoBase, Authentiztion: AuthJWT = Depends()):
    # try:
    #     Authentiztion.jwt_required()
    #
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')
    #
    # check_user_token = Authentiztion.get_jwt_subject()
    # check_user = session.query(User).filter(User.username == check_user_token).first()
    # if check_user.is_superuser:
    adr_check = session.query(UserInfo).filter(UserInfo.id == id).first()
    new_id_check = session.query(UserInfo).filter(UserInfo.id == user.id).first()
    user_id = session.query(User).filter(User.id == user.user_id).first()
    if adr_check:
        if user_id:
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
# return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Only admins can edit this address')


@user_info_router.delete('/{id}')
async def delete_user(id: int, Authentiztion: AuthJWT = Depends()):
    # try:
    #     Authentiztion.jwt_required()
    #
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    # check_user_token = Authentiztion.get_jwt_subject()
    # check_user = session.query(User).filter(User.username == check_user_token).first()
    # if check_user.is_superuser:
    item = session.query(UserInfo).filter(UserInfo.id == id).first()
    if item:
        session.delete(item)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Deleted")

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Malumot topilmadi")
    # return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only admins can delete this address")
