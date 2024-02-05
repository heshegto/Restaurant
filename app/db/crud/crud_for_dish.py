from sqlalchemy.orm import Session
from app.business import schemas
from app.db import models
from uuid import UUID


def get_dishes(db: Session, submenu_id: UUID):
    return db.query(models.Dish).filter(models.Dish.id_submenu == submenu_id)


def get_dish_by_id(db: Session, dish_id: UUID, submenu_id: UUID):
    return get_dishes(db, submenu_id).filter(models.Dish.id == dish_id).first()


def create_dish(db: Session, submenu_id: UUID, dish: schemas.DishCreate):
    db_dish = models.Dish(
        title=dish.title,
        description=dish.description,
        price="{:.2f}".format(round(float(dish.price), 2)),
        id_submenu=submenu_id
    )
    db.add(db_dish)
    db.commit()
    return db_dish


def patch_dish(db: Session, dish_id: UUID, submenu_id: UUID, dish: schemas.DishCreate):
    dish_to_update = get_dish_by_id(db, dish_id, submenu_id)
    if dish_to_update:
        dish_to_update.title = dish.title
        dish_to_update.description = dish.description
        dish_to_update.price = "{:.2f}".format(round(float(dish.price), 2))
        db.commit()
        db.refresh(dish_to_update)
    return dish_to_update


def delete_dish(db: Session, dish_id: UUID, submenu_id: UUID):
    dish_to_delete = get_dish_by_id(db, dish_id, submenu_id)
    if dish_to_delete:
        db.delete(dish_to_delete)
        db.commit()
    return dish_to_delete