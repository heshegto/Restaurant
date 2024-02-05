from sqlalchemy import Column, ForeignKey, String, UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    title = Column(String)
    description = Column(String, nullable=True)


class Menu(BaseModel):
    __tablename__ = "menus"
    child_menu = relationship("SubMenu", back_populates="parent_menu", cascade="all, delete-orphan")


class SubMenu(BaseModel):
    __tablename__ = "submenus"

    id_menu = Column(UUID(as_uuid=True), ForeignKey("menus.id", ondelete="CASCADE"))

    parent_menu = relationship("Menu", back_populates="child_menu")
    dish = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")


class Dish(BaseModel):
    __tablename__ = "dishes"

    price = Column(String)
    id_submenu = Column(UUID(as_uuid=True), ForeignKey("submenus.id"))

    submenu = relationship("SubMenu", back_populates="dish")