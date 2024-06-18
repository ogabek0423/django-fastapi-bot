from fastapi import APIRouter
from database import Session, ENGINE
from schemas import *
from db_models import *
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from django.contrib.auth.hashers import make_password, check_password


session = Session(bind=ENGINE)

cupon_router = APIRouter(prefix="/coupons", tags=["coupons"])


@cupon_router.get("/")
async def get_all():
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        c_list = session.query(Coupon).all()
        context = [
            {
                "id": c.id,
                "code": c.code,
                "value": c.value
            }
            for c in c_list
        ]
        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@cupon_router.get("/{id}")
async def get_c(id: int):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        c = session.query(Coupon).filter(Coupon.id == id).first()
        context = [
            {
                "id": c.id,
                "code": c.code,
                "value": c.value
            }
        ]
        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='unauthorized')


@cupon_router.post('/create')
async def create_c(cup: CouponBase, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        c_check = session.query(Coupon).filter(Coupon.id == cup.id).first()
        if c_check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")

        new_c = Coupon(
            id=cup.id,
            code=cup.code,
            value=cup.value
        )
        session.add(new_c)
        session.commit()
        return HTTPException(status_code=status.HTTP_201_CREATED, detail="cat created successfully")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="only admin has permission")


@cupon_router.put("/{id}")
async def update_c(id: int, c: CouponBase, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        check = session.query(Coupon).filter(Coupon.id == id).first()
        check_id = session.query(Coupon).filter(Coupon.id == c.id).first()
        if check:
            if check_id is None or check_id.id == id:
                for key, value in c.dict(exclude_unset=True).items():
                    setattr(check, key, value)
                    session.commit()

                data = {
                    "code": 200,
                    "message": "update c"
                }
                return jsonable_encoder(data)

            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="yangi berilgan id da malumot mavjud!")

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='only admins can update city')


@cupon_router.delete("/{id}")
async def delete_c(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        check = session.query(Coupon).filter(Coupon.id == id).first()
        if check:
            session.delete(check)
            session.commit()
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Deleted")

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='only admins can delete city')

