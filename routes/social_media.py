from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.social_media import one_social_media, all_social_medias, create_social_media, update_social_media, social_media_delete
from schemas.social_media import *
from schemas.users import UserCurrent

router_social_media = APIRouter()


@router_social_media.post('/add', )
def add_social_media(form: SocialMediaBase, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: CustomerBase = Depends(get_current_active_user)
    if create_social_media(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_social_media.get('/', status_code=200)
def get_social_medias(search: str = None, status: bool = True, id: int = 0, page: int = 1, limit: int = 25,
             db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return one_social_media(id, db)
    else:
        return all_social_medias(search, status, page, limit, db, )


@router_social_media.put("/update")
def social_media_update(form: SocialMediaUpdate, db: Session = Depends(get_db),
               current_user: UserCurrent = Depends(get_current_active_user)):
    if update_social_media(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_social_media.delete('/{id}', status_code=200)
def delete_social_media(id: int = 0, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return social_media_delete(id, current_user, db)


