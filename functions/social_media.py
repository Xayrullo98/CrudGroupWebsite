from fastapi import HTTPException
from functions import orders
from functions.users import one_user
from models.social_media import SocialMedia
from utils.pagination import pagination


def all_social_medias(search, status, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = SocialMedia.name.like(search_formatted) | SocialMedia.link.like(
            search_formatted)
    else:
        search_filter = SocialMedia.id > 0
    if status in [True, False]:
        status_filter = SocialMedia.status == status
    else:
        status_filter = SocialMedia.status.in_([True, False])

    social_media = db.query(SocialMedia).filter(search_filter, status_filter).order_by(SocialMedia.id.desc())
    if page and limit:
        return pagination(social_media, page, limit)
    else:
        return social_media.all()


def one_social_media(id, db):
    return db.query(SocialMedia).filter(SocialMedia.id == id).first()

def last_social_media(db):
    return db.query(SocialMedia).filter(SocialMedia.status==True).order_by(SocialMedia.id.desc()).first()

def create_social_media(form, user, db):
    new_social_media_db = SocialMedia(
        name=form.name,
        link=form.link,
        user_id=user.id,

    )

    db.add(new_social_media_db)
    db.commit()


    return new_social_media_db


def update_social_media(form, user, db):
    if one_social_media(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli mahsulot mavjud emas")

    if one_user(user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(SocialMedia).filter(SocialMedia.id == form.id).update({
        SocialMedia.name: form.name,
        SocialMedia.link: form.link,
        SocialMedia.status: form.status,
        SocialMedia.user_id: user.id,
    })
    db.commit()
    return one_social_media(form.id, db)


def social_media_delete(id, user, db):
    if one_social_media(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli mahsulot mavjud emas")
    db.query(SocialMedia).filter(SocialMedia.id == id).update({
        SocialMedia.status: False,
        SocialMedia.user_id: user.id
    })
    db.commit()
    return {"date": "Mahsulot o'chirildi !"}