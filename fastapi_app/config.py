from fastapi import FastAPI
from auth import a_router
from schemas import JwtModel
from fastapi_jwt_auth import AuthJWT
from crud.users import user_router
from crud.coupon import cupon_router
from crud.problem import problem_router
from crud.category import category_router
from crud.payments import pay_router
from crud.products import product_router
from crud.userinfo import user_info_router
from crud.staffinfo import staff_info_router
from crud.telegramuser import tg_router
from crud.blog import blog_router


app = FastAPI()
app.include_router(a_router)
app.include_router(user_router)
app.include_router(cupon_router)
app.include_router(product_router)
app.include_router(problem_router)
app.include_router(category_router)
app.include_router(pay_router)
app.include_router(user_info_router)
app.include_router(staff_info_router)
app.include_router(blog_router)
app.include_router(tg_router)


@AuthJWT.load_config
def get_config():
    return JwtModel()


@app.get('/')
async def root():
    return {"message": "root xabari"}


@app.get('/items')
async def read_items():
    return {'message': 'test api items'}


@app.get('/userx')
async def user():
    return {'message': 'user page'}


@app.get('/userx/{id}')
async def read_user(id: int):
    return {'message': f'user id = {id}'}

