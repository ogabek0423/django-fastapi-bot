from fastapi import APIRouter
from database import Session, ENGINE
from schemas import *
from db_models import *
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT


session = Session(bind=ENGINE)
pay_router = APIRouter(prefix="/payment")


@pay_router.get('/')
async def get_all_payments():
    # try:
    #     Authentiztion.jwt_required()
    #
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')
    #
    # check_user_token = Authentiztion.get_jwt_subject()
    # check_user = session.query(User).filter(User.username == check_user_token).first()
    # if check_user.is_active:
    payments = session.query(Payment).all()
    context = [
        {
            "id": payment.id,
            "amount": payment.amount,
            "user": {
                "id": payment.user.id,
                "first_name": payment.user.first_name,
                "last_name": payment.user.last_name,
                "username": payment.user.username,
                "email": payment.user.email
            },
            "type": payment.pay_type,
            "product_list": payment.product_list,
            "coupon": {
                "id": payment.coupon.id,
                "code": payment.coupon.code,
                "value": payment.coupon.value
            },
            "pay_time": payment.pay_time

        }
        for payment in payments
    ]
    return jsonable_encoder(context)
# return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")


@pay_router.get('/{id}')
async def get_one_payment(id: int):
    # try:
    #     Authentiztion.jwt_required()
    #
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')
    #
    # check_user_token = Authentiztion.get_jwt_subject()
    # check_user = session.query(User).filter(User.username == check_user_token).first()
    # if check_user.is_active:
    payment = session.query(Payment).filter(Payment.user_id == id).first()
    data = {
             "id": payment.id,
            "amount": payment.amount,
            "user": {
                "id": payment.user.id,
                "first_name": payment.user.first_name,
                "last_name": payment.user.last_name,
                "username": payment.user.username,
                "email": payment.user.email
            },
            "type": payment.pay_type,
            "product_list": payment.product_list,
            "coupon": {
                "id": payment.coupon.id,
                "code": payment.coupon.code,
                "value": payment.coupon.value
            },
            "pay_time": payment.pay_time
    }

    return jsonable_encoder(data)
# return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@pay_router.get('/user_pays/{id}')
async def get_user_pays(id: int, Authentiztion: AuthJWT = Depends()):
    # try:
    #     Authentiztion.jwt_required()
    #
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')
    #
    # check_user_token = Authentiztion.get_jwt_subject()
    # check_user = session.query(User).filter(User.username == check_user_token).first()
    # if check_user.is_active:
    payments = session.query(Payment).filter(Payment.user_id == id).all()
    if payments:
        context = [
            {
                "id": payment.id,
                "amount": payment.amount,
                "user": {
                    "id": payment.user.id,
                    "first_name": payment.user.first_name,
                    "last_name": payment.user.last_name,
                    "username": payment.user.username,
                    "email": payment.user.email
                },
                "type": payment.pay_type,
                "product_list": payment.product_list,
                "coupon": {
                    "id": payment.coupon.id,
                    "code": payment.coupon.code,
                    "value": payment.coupon.value
                },
                "pay_time": payment.pay_time
            }
            for payment in payments
        ]
        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment does not exist")
    # return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@pay_router.get('/user_total_pay/{id}')
async def user_total_pay(id:int, Authentiztion: AuthJWT = Depends()):
    # try:
    #     Authentiztion.jwt_required()
    #
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')
    #
    # check_user_token = Authentiztion.get_jwt_subject()
    # check_user = session.query(User).filter(User.username == check_user_token).first()
    # if check_user.is_active:
    payments = session.query(Payment).filter(Payment.user_id == id).all()
    if payments:
        count = len(payments)
        total = 0
        name = ''
        for payment in payments:
            total += payment.amount
            name = payment.user.username
        data = {
            "foydalanuvchi": name,
            "total pay": total,
            "count pay": count
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data does not exist")
    # return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@pay_router.post('/create')
async def create_payment(payment: PaymentBase, Authentiztion: AuthJWT = Depends()):
    # try:
    #     Authentiztion.jwt_required()
    #
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')
    #
    # check_user_token = Authentiztion.get_jwt_subject()
    # check_user = session.query(User).filter(User.username == check_user_token).first()
    # if check_user.is_superuser:
    check = session.query(Payment).filter(Payment.id == payment.id).first()
    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment already exists")

    new_payment = Payment(
        id=payment.id,
        amount=payment.amount,
        pay_type=payment.pay_type,
        user_id=payment.user_id,
        coupon_id=payment.coupon_id,
        product_list=payment.product_list

    )
    session.add(new_payment)
    session.commit()
    payment = new_payment
    data = {
         {"msg": "Payment created",
             "id": payment.id,
                "amount": payment.amount,
                "user": {
                    "id": payment.user.id,
                    "first_name": payment.user.first_name,
                    "last_name": payment.user.last_name,
                    "username": payment.user.username,
                    "email": payment.user.email
                },
                "type": payment.pay_type,
                "product_list": payment.product_list,
                "coupon": {
                    "id": payment.coupon.id,
                    "code": payment.coupon.code,
                    "value": payment.coupon.value
                },
                "pay_time": payment.pay_time
         }
            if payment.user else None
            if payment.coupon else None

    }
    return HTTPException(status_code=status.HTTP_201_CREATED, detail=data)
    # return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can create")


@pay_router.put('/{id}')
async def update_payment(id: int, update: PaymentBase, Authentiztion: AuthJWT = Depends()):
    # try:
    #     Authentiztion.jwt_required()
    #
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')
    #
    # check_user_token = Authentiztion.get_jwt_subject()
    # check_user = session.query(User).filter(User.username == check_user_token).first()
    # if check_user.is_superuser:
    check = session.query(Payment).filter(Payment.id == id).first()
    new_id = session.query(Payment).filter(Payment.id == update.id).first()
    user_id = session.query(User).filter(User.id == update.user_id).first()

    if check:
        if new_id is None or new_id.id == update.id:
            if user_id:
                for key, value in update.dict().items():
                    setattr(check, key, value)
                    session.commit()
                payment = check
                data = {
                    "id": payment.id,
                    "amount": payment.amount,
                    "user": {
                        "id": payment.user.id,
                        "first_name": payment.user.first_name,
                        "last_name": payment.user.last_name,
                        "username": payment.user.username,
                        "email": payment.user.email
                    },
                    "type": payment.pay_type,
                    "product_list": payment.product_list,
                    "coupon": {
                        "id": payment.coupon.id,
                        "code": payment.coupon.code,
                        "value": payment.coupon.value
                    },
                    "pay_time": payment.pay_time
                }
                return jsonable_encoder(data)
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday user mavjud emas!")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Berilgan yangi id da malumot mavjud!")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" malumot topilmadi!")
    # return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can")


@pay_router.delete("/{id}")
async def delete_payment(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        item = session.query(Payment).filter(Payment.id == id).first()
        if item:
            session.delete(item)
            session.commit()
            data = {"message": "Payment deleted successfully"}
            return jsonable_encoder(data)

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can")