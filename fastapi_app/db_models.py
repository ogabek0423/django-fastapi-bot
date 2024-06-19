from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from database import Base, Session



class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=datetime.datetime.utcnow)
    user_info = relationship("UserInfo", back_populates="user")
    staff_info = relationship("StaffInfo", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    blog = relationship("Blog", back_populates="user")



class TelegramUser(Base):
    __tablename__ = 'telegram_users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150))
    fullname = Column(String(150))
    chat_id = Column(Integer)
    created_time = Column(DateTime, default=datetime.datetime.utcnow)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    last_update = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    product = relationship("Product", back_populates="category")
    slug = Column(String, unique=True)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    image = Column(String)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='product')
    price = Column(Numeric(10, 2))
    count = Column(Integer)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    endurance = Column(Integer)
    slug = Column(String, unique=True)


class Coupon(Base):
    __tablename__ = 'coupons'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50))
    value = Column(Numeric(10, 2))
    pay = relationship("Payment", back_populates="coupon")

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('auth_user.id'))
    user = relationship('User', back_populates='payments')
    product_list = Column(Text)
    amount = Column(Numeric(10, 2))
    pay_type = Column(String(50))
    pay_time = Column(DateTime, default=datetime.datetime.utcnow)
    coupon_id = Column(Integer, ForeignKey('coupons.id'))
    coupon = relationship('Coupon', back_populates='pay')

class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('auth_user.id'))
    user = relationship('User', back_populates='user_info')
    your_photo = Column(String)
    city = Column(String(100))
    street = Column(String(100))
    home_number = Column(String(50))
    user_number = Column(String(20))
    last_update = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class StaffInfo(Base):
    __tablename__ = 'staff_info'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('auth_user.id'))
    user = relationship('User', back_populates='staff_info')
    photo = Column(String)
    work_time = Column(String(100))
    phone = Column(String(20))
    experience = Column(Text)
    slug = Column(String, unique=True)

class Blog(Base):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    user_id = Column(Integer, ForeignKey('auth_user.id'))
    user = relationship('User', back_populates='blog')
    created_time = Column(DateTime, auto_now_add=True)
    slug = Column(String, max_length=100, unique=True)

class Problem(Base):
    __tablename__ = 'problems'
    id = Column(Integer, primary_key=True, index=True)
    problem_text = Column(Text)
    user_email = Column(String, index=True)
    created_time = Column(DateTime, default=datetime.datetime.utcnow)
    slug = Column(String, max_length=100, unique=True)