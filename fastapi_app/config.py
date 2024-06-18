from fastapi import FastAPI
from auth import a_router
from crud.users import user_router
from schemas import JwtModel
from fastapi_jwt_auth import AuthJWT


app = FastAPI()
app.include_router(a_router)
app.include_router(user_router)


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

