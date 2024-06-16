from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, DECIMAL
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    your_photo = Column(String)
    city = Column(String)
    street = Column(String)
    home_number = Column(String)
    user_number = Column(String)
    last_update = Column(DateTime, default=datetime.datetime.utcnow)


class StaffInfo(Base):
    __tablename__ = "staff_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    photo = Column(String)
    work_time = Column(String)
    phone = Column(String)
    experience = Column(Text)


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    fullname = Column(String)
    chat_id = Column(String)
    created_time = Column(DateTime, default=datetime.datetime.utcnow)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_update = Column(DateTime, default=datetime.datetime.utcnow)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("category.id"))
    price = Column(DECIMAL)
    count = Column(Integer)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    endurance = Column(Integer)


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    value = Column(DECIMAL)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_list = Column(Text)
    amount = Column(DECIMAL)
    pay_type = Column(String)
    pay_time = Column(DateTime, default=datetime.datetime.utcnow)
    coupon_id = Column(Integer, ForeignKey("coupons.id"))


class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_time = Column(DateTime, default=datetime.datetime.utcnow)


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    problem_text = Column(Text)
    user_email = Column(String)
    created_time = Column(DateTime, default=datetime.datetime.utcnow)
