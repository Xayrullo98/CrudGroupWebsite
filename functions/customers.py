from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.orders import Orders
from models.phones import Phones
from models.social_media import SocialMedia
from models.users import Users
from models.customers import Customers

from utils.pagination import pagination


def all_customers(search, status, user_id, hide, page, limit, db):
    if search:
        search_formatted="%{}%".format ( search )
        search_filter=Customers.name.like ( search_formatted ) | Customers.address.like (
            search_formatted ) | Phones.number.like ( search_formatted )


    else:
        search_filter=Customers.id > 0

    if status in [True, False]:
        status_filter=Customers.status == status
    else:
        status_filter=Customers.status.in_ ( [True, False] )

    if user_id:
        user_id_filter=Customers.user_id == user_id
    else:
        user_id_filter=Customers.id > 0

    if hide:
        customers=db.query ( Customers ).join ( Phones ).options (
            joinedload ( Customers.social ).load_only ( SocialMedia.name, SocialMedia.link ),
            joinedload ( Customers.phones ).load_only ( Phones.number, Phones.comment ),
            joinedload ( Customers.orders ).load_only ( Orders.customer_id, Orders.savdo_id ), ).filter ( search_filter,
                                                                                                          status_filter,
                                                                                                          user_id_filter,
                                                                                                          Orders.customer_id != None
                                                                                                          ).order_by (
            Customers.id.desc ( ) )

        if page and limit:
            return pagination ( customers, page, limit )
        else:
            return customers.all ( )

    else:
        customers=db.query ( Customers ).join ( Phones ).outerjoin ( Orders ).options (
			joinedload ( Customers.social ).load_only ( SocialMedia.name, SocialMedia.link ),
            joinedload ( Customers.phones ).load_only ( Phones.number, Phones.comment ),
            joinedload ( Customers.orders ).load_only ( Orders.customer_id, Orders.savdo_id ) ).filter ( search_filter,
                                                                                                         status_filter,
                                                                                                         user_id_filter,
                                                                                                         ).order_by (
            Customers.id.desc ( ) )

        if page and limit:
            return pagination ( customers, page, limit )
        else:
            return customers.all ( )


def one_customer(id, db):
    return db.query ( Customers ).options (
        joinedload ( Customers.social ).load_only ( SocialMedia.name, SocialMedia.link ),
        joinedload ( Customers.phones ).load_only ( Phones.number, Phones.comment ),
        joinedload ( Customers.orders ).load_only ( Orders.customer_id, Orders.savdo_id ) ).filter (
        Customers.id == id ).first ( )


def create_customer(form, user, db):
    new_customer_db=Customers (
        name=form.name,
        address=form.address,
        user_id=user.id,
    )
    db.add ( new_customer_db )
    db.commit ( )

    for phone in form.phones:
        phone_verification=db.query ( Phones ).filter ( Phones.number == phone.number ).first ( )
        if phone_verification:
            raise HTTPException ( status_code=400, detail="Bunday telefon raqam mavjud" )
        new_phone_db=Phones (
            number=phone.number,
            source_id=new_customer_db.id,
            comment=phone.comment,
            user_id=user.id
        )
        db.add ( new_phone_db )
        db.commit ( )
    for social in form.social_medias:
        phone_verification=db.query ( SocialMedia ).filter ( SocialMedia.link == social.link ).first ( )
        if phone_verification:
            raise HTTPException ( status_code=400, detail="Bunday link mavjud" )
        new_phone_db=SocialMedia (
            name=social.name,
            source_id=new_customer_db.id,
            link=social.link,
            user_id=user.id
        )
        db.add ( new_phone_db )
        db.commit ( )

    return new_customer_db


def update_customer(form, user, db):
    if one_customer ( form.id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli mijoz mavjud emas" )

    db.query ( Customers ).options (
        joinedload ( Customers.phones ).load_only ( Phones.number, Phones.comment ) ).filter (
        Customers.id == form.id ).update ( {
        Customers.name: form.name,
        Customers.address: form.address,
        Customers.status: form.status,
        Customers.user_id: user.id,

    } )
    db.commit ( )
    db.query ( Phones ).filter ( Phones.source_id == form.id ).delete ( )
    for phone in form.phones:
        new_phone_db=Phones (
            number=phone.number,
            source_id=form.id,
            comment=phone.comment,
            user_id=user.id
        )
        db.add ( new_phone_db )
        db.commit ( )

    db.query ( SocialMedia ).filter ( SocialMedia.source_id == form.id ).delete ( )
    for phone in form.social_medias:
        new_phone_db=SocialMedia (
            name=phone.name,
            source_id=form.id,
            link=phone.link,
            user_id=user.id
        )
        db.add ( new_phone_db )
        db.commit ( )

    return one_customer ( form.id, db )


def customer_delete(id, user, db):
    if one_customer ( id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli customer mavjud emas" )
    db.query ( Customers ).filter ( Customers.id == id ).update ( {
        Customers.status: False,
        Customers.user_id: user.id
    } )
    db.commit ( )
    return {"date": "Customer o'chirildi !"}


def hide_passive_customers(user, db):
    db.query ( Customers ).filter ( Customers.id != Orders.customer_id ).update ( {
        Customers.status: False,
        Customers.user_id: user.id
    } )
    db.commit ( )
    return {"date": "Done"}


def show_passive_customers(user, db):
    db.query ( Customers ).filter ( Customers.id != Orders.customer_id ).update ( {
        Customers.status: True,
        Customers.user_id: user.id
    } )
    db.commit ( )
    return {"date": "Done"}
