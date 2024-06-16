from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    password: str
    email: str
    is_staff: bool = False
    is_active: bool = True
    is_superuser: bool = False
    id: int

    class Config:
        orm_mode = True

class UserInfoBase(BaseModel):
    your_photo: Optional[str]
    city: str
    street: str
    home_number: str
    user_number: str
    last_update: Optional[datetime]
    user_id: int
    id: int

    class Config:
        orm_mode = True

class StaffInfoBase(BaseModel):
    photo: Optional[str]
    work_time: str
    phone: str
    experience: str
    user_id: int
    id: int

    class Config:
        orm_mode = True

class TelegramUserBase(BaseModel):
    id: Optional[id]
    username: str
    fullname: str
    chat_id: str
    created_time: Optional[datetime]

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str
    last_update: Optional[datetime]
    id: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: str
    category_id: int
    price: float
    count: int
    created_date: Optional[datetime]
    endurance: int
    id: int

    class Config:
        orm_mode = True

class CouponBase(BaseModel):
    code: str
    value: float
    id: int

    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    product_list: str
    amount: float
    pay_type: str
    pay_time: Optional[datetime]
    coupon_id: Optional[int]
    user_id: int
    id: int

    class Config:
        orm_mode = True

class BlogBase(BaseModel):
    text: str
    created_time: Optional[datetime]
    user_id: int
    id: int

    class Config:
        orm_mode = True

class ProblemBase(BaseModel):
    problem_text: str
    user_email: str
    created_time: Optional[datetime]
    id: int

    class Config:
        orm_mode = True
