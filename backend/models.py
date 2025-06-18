from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=True)


class Product(Base):
    __tablename__ = "product"
    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    price: Mapped[str] = mapped_column(Integer)
    isForMen: Mapped[str] = mapped_column(Boolean)
    isForWomen: Mapped[str] = mapped_column(Boolean)
    sizesOnStock: Mapped[str] = mapped_column(String(255), nullable=True)


class ProductsBought(Base):
    __tablename__ = "products_bought"
    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    productId: Mapped[str] = mapped_column(Integer, nullable=False)
    userId: Mapped[str] = mapped_column(Integer, nullable=False)
    size: Mapped[str] = mapped_column(Integer, nullable=False)


class ProductsInBag(Base):
    __tablename__ = "products_in_bag"
    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    productId: Mapped[str] = mapped_column(Integer, nullable=False)
    userId: Mapped[str] = mapped_column(Integer, nullable=False)
    size: Mapped[str] = mapped_column(Integer, nullable=False)


class Sessions(Base):
    __tablename__ = "sessions"
    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    sessionId: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    userId: Mapped[str] = mapped_column(Integer, nullable=False)
