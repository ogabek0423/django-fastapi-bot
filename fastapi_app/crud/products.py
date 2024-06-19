from fastapi import APIRouter
from database import Session, ENGINE
from schemas import *
from db_models import *
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT


session = Session(bind=ENGINE)

product_router = APIRouter(prefix="/product")


@product_router.get('/')
async def get_products(Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        products = session.query(Product).all()
        return jsonable_encoder(products)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

@product_router.get('/{id}')
async def get_product(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        product = session.query(Product).filter(Product.id == id).first()
        return jsonable_encoder(product)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

@product_router.post('/create')
async def create_product(product: ProductBase, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        product_c = session.query(Product).filter(Product.id == product.id).first()
        cat = session.query(Category).filter(Category.id == product.category_id)
        if not product_c:
            if cat:
                new_product = Product(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    category_id=product.category_id,
                    count=product.count,
                    endurance=product.endurance,
                    image=product.image
                )
                session.add(new_product)
                session.commit()
                return jsonable_encoder(new_product, detail="Product created successfully")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category is not")
        else:
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product already exists")
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="only admin user is allowed to")

@product_router.put('/{id}')
async def update(id: int, product: ProductBase, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        adr_check = session.query(Product).filter(Product.id == id).first()
        new_id_check = session.query(Product).filter(Product.id == product.id).first()
        cat_check = session.query(Category).filter(Category.id == product.category_id).first()
        if adr_check:
            if cat_check:
                if new_id_check is None:
                    for key, value in product.dict().items():
                        setattr(adr_check, key, value)
                        session.commit()

                    data = {
                        "code": 200,
                        "message": "product updated"
                    }
                    return jsonable_encoder(data)
                elif new_id_check.id == adr_check.id:
                    for key, value in product.dict().items():
                        setattr(adr_check, key, value)
                        session.commit()

                    data = {
                        "code": 200,
                        "message": "product updated"
                    }
                    return jsonable_encoder(data)
                return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Berilgan id da malumot mavjud!")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="berilgan city id mavjud emas!")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malumot topilmadi")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Only admins can edit this address')


@product_router.delete('/{id}')
async def delete(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        item = session.query(Product).filter(Product.id == id).first()
        if item:
            session.delete(item)
            session.commit()
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Deleted")

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Malumot topilmadi")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only admins can delete this address")

