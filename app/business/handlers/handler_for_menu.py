from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from app.db.database import get_db

from uuid import UUID
from fastapi import APIRouter
from app.db.cache_database import get_redis
from redis import Redis
from app.db.db_loaders import db_loader_for_menu as db_loader
router = APIRouter()


@router.get('/api/v1/menus', response_model=list[schemas.MenuRead])
def read_menus(db: Session = Depends(get_db), cache: Redis = Depends(get_redis)):
    return db_loader.get_all_menus(db, cache)


@router.get('/api/v1/menus/{target_menu_id}', response_model=schemas.MenuRead)
def read_menu_by_id(target_menu_id: UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_redis)):
    db_menu = db_loader.get_one_menu(target_menu_id, db, cache)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu


@router.post('/api/v1/menus', response_model=schemas.Menu, status_code=201)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db), cache: Redis = Depends(get_redis)):
    return db_loader.create_menu(menu, db, cache)


@router.patch('/api/v1/menus/{target_menu_id}', response_model=schemas.Menu)
def update_menu(target_menu_id: UUID, menu: schemas.MenuCreate, db: Session = Depends(get_db), cache: Redis= Depends(get_redis)):
    return db_loader.update_menu(target_menu_id, menu, db, cache)


@router.delete('/api/v1/menus/{target_menu_id}', response_model=schemas.Menu)
def delete_menu(target_menu_id: UUID, db: Session = Depends(get_db), cache: Redis= Depends(get_redis)):
    return db_loader.delete_menu(target_menu_id, db, cache)
