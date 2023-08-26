import typing
import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from typing import List
import shutil

from db import Base, engine, get_db
from typing import Optional
from sqlalchemy.orm import Session


from functions.uploaded_files import create_uploaded_file, one_uploaded_file_via_source
from functions.users import one_user
from models.orders import Orders
from models.trades import Trades
from routes.auth import get_current_active_user
from utils.pagination import status_dict

Base.metadata.create_all ( bind=engine )

from functions.orders import one_order, all_orders, create_order, update_order,  update_order_status, \
     returned_products

from schemas.orders import *
from schemas.users import UserCurrent

router_order=APIRouter ( )


@router_order.post ( '/add', )
def add_order(form: OrderCreate, db: Session = Depends ( get_db ), current_user: UserCurrent = Depends (
    get_current_active_user )):  # current_user: CustomerBase = Depends(get_current_active_user)

    return create_order ( form, current_user, db )


@router_order.get ( '/', status_code=200 )
def get_orders(search: str = None, status: bool = True, userid: int = 0, customerid: int = 0, id: int = 0,
               season_id: int = 0, order_status: str = None,
               page: int = 1, start_date=None, end_date=None,
               limit: int = 25, db: Session = Depends ( get_db ), current_user: UserCurrent = Depends (
            get_current_active_user )):  # current_user: User = Depends(get_current_active_user)
    if not id:

        return all_orders ( search=search, userid=userid, customerid=customerid, status=status,
                            order_status=order_status,
                            season_id=season_id, page=page, limit=limit, db=db, start_date=start_date,
                            end_date=end_date,
                            )
    else:
        return one_order ( id, db )


@router_order.put ( "/update" )
def order_update(form: OrderUpdate, db: Session = Depends ( get_db ),
                 current_user: UserCurrent = Depends ( get_current_active_user )):
    if update_order ( form, current_user, db ):
        raise HTTPException ( status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi" )


@router_order.put ( "/status" )
def order_s(id: int = Body ( ..., ge=0 ),
            comment: typing.Optional[str] = Body ( '' ),
            source: typing.Optional[str] = Body ( '' ),
            files: typing.Optional[List[UploadFile]] = File ( None ), db: Session = Depends ( get_db ),
            current_user: UserCurrent = Depends ( get_current_active_user )):
    order=one_order ( id=id, db=db )
    order_status = status_dict.get(source)
    user=one_user ( id=current_user.id, db=db )

    if source == 'created':
        db.query ( Orders ).filter ( Orders.id == id ).update ( {
            Orders.id: id,
            Orders.user_id: user.id,
            Orders.order_status: order_status,
            Orders.updated_day: datetime.datetime.now ( ).date ( ),
            Orders.created_date: datetime.datetime.now ( ).date ( )} )
        db.commit ( )
        if files:
            for file in files:
                with open ( "media/" + file.filename, 'wb' ) as image:
                    shutil.copyfileobj ( file.file, image )
                url=str ( 'media/' + file.filename )
                create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                       user=current_user, db=db )
    elif source=="payment":
        db.query ( Orders ).filter ( Orders.id == id ).update ( {
            Orders.id: id,
            Orders.user_id: user.id,
            Orders.order_status: order_status,
            Orders.updated_day: datetime.datetime.now ( ).date ( ),
            Orders.payment_date: datetime.datetime.now ( ).date ( )} )
        db.commit ( )
        if files:
            for file in files:
                with open ( "media/" + file.filename, 'wb' ) as image:
                    shutil.copyfileobj ( file.file, image )
                url=str ( 'media/' + file.filename )
                create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                       user=current_user, db=db )
    elif source=="design":
        db.query ( Orders ).filter ( Orders.id == id ).update ( {
            Orders.id: id,
            Orders.user_id: user.id,
            Orders.order_status: 'programming',
            Orders.updated_day: datetime.datetime.now ( ).date ( ),
            Orders.land_preparation_date: datetime.datetime.now ( ).date ( )} )
        db.commit ( )
        if files:
            for file in files:
                with open ( "media/" + file.filename, 'wb' ) as image:
                    shutil.copyfileobj ( file.file, image )
                url=str ( 'media/' + file.filename )
                create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                       user=current_user, db=db )
    elif source=="programming" :
        db.query ( Orders ).filter ( Orders.id == id ).update ( {
            Orders.id: id,
            Orders.user_id: user.id,
            Orders.order_status: 'deploy',
            Orders.updated_day: datetime.datetime.now ( ).date ( ),
            Orders.land_preparation_date: datetime.datetime.now ( ).date ( )} )
        db.commit ( )
        if files:
            for file in files:
                with open ( "media/" + file.filename, 'wb' ) as image:
                    shutil.copyfileobj ( file.file, image )
                url=str ( 'media/' + file.filename )
                create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                       user=current_user, db=db )
    elif source=="overheads" and order.land_preparation_date:
        db.query ( Orders ).filter ( Orders.id == id ).update ( {
            Orders.id: id,
            Orders.user_id: user.id,
            Orders.order_status: order_status,
            Orders.updated_day: datetime.datetime.now ( ).date ( ),
            Orders.overheads_date: datetime.datetime.now ( ).date ( )} )
        db.commit ( )
        if files:
            for file in files:
                with open ( "media/" + file.filename, 'wb' ) as image:
                    shutil.copyfileobj ( file.file, image )
                url=str ( 'media/' + file.filename )
                create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                       user=current_user, db=db )
    elif source=="overheads" :
        db.query ( Orders ).filter ( Orders.id == id ).update ( {
            Orders.id: id,
            Orders.user_id: user.id,
            Orders.order_status: 'land_preparation',
            Orders.updated_day: datetime.datetime.now ( ).date ( ),
            Orders.overheads_date: datetime.datetime.now ( ).date ( )} )
        db.commit ( )
        if files:
            for file in files:
                with open ( "media/" + file.filename, 'wb' ) as image:
                    shutil.copyfileobj ( file.file, image )
                url=str ( 'media/' + file.filename )
                create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                       user=current_user, db=db )
    elif source=="upload_products":
        db.query ( Orders ).filter ( Orders.id == id ).update ( {
            Orders.id: id,
            Orders.user_id: user.id,
            Orders.order_status: order_status,
            Orders.updated_day: datetime.datetime.now ( ).date ( ),
            Orders.upload_products_date: datetime.datetime.now ( ).date ( )} )
        db.commit ( )
        if files:
            for file in files:
                with open ( "media/" + file.filename, 'wb' ) as image:
                    shutil.copyfileobj ( file.file, image )
                url=str ( 'media/' + file.filename )
                create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                       user=current_user, db=db )
    elif source=="reception":
        db.query ( Orders ).filter ( Orders.id == id ).update ( {
            Orders.id: id,
            Orders.user_id: user.id,
            Orders.order_status: order_status,
            Orders.updated_day: datetime.datetime.now ( ).date ( ),
            Orders.reception_date: datetime.datetime.now ( ).date ( )} )
        db.commit ( )
        if files:
            for file in files:
                with open ( "media/" + file.filename, 'wb' ) as image:
                    shutil.copyfileobj ( file.file, image )
                url=str ( 'media/' + file.filename )
                create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                       user=current_user, db=db )
    elif source=="rules":
        db.query ( Orders ).filter ( Orders.id == id ).update ( {
            Orders.id: id,
            Orders.user_id: user.id,
            Orders.order_status: order_status,
            Orders.updated_day: datetime.datetime.now ( ).date ( ),
            Orders.rules_date: datetime.datetime.now ( ).date ( )} )
        db.commit ( )
        if files:
            for file in files:
                with open ( "media/" + file.filename, 'wb' ) as image:
                    shutil.copyfileobj ( file.file, image )
                url=str ( 'media/' + file.filename )
                create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                       user=current_user, db=db )
    elif source=="planting":
        db.query ( Orders ).filter ( Orders.id == id ).update ( {
            Orders.id: id,
            Orders.user_id: user.id,
            Orders.order_status: order_status,
            Orders.updated_day: datetime.datetime.now ( ).date ( ),
            Orders.planting_date: datetime.datetime.now ( ).date ( )} )
        db.commit ( )
        if files:
            for file in files:
                with open ( "media/" + file.filename, 'wb' ) as image:
                    shutil.copyfileobj ( file.file, image )
                url=str ( 'media/' + file.filename )
                create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                       user=current_user, db=db )
    elif source=="control":
        if not order.day1:
            db.query ( Orders ).filter ( Orders.id == id ).update ( {
                Orders.id: id,
                Orders.user_id: current_user.id,
                Orders.day1: datetime.datetime.now ( ).date ( ), } )
            db.commit ( )
            if files:
                for file in files:
                    with open ( "media/" + file.filename, 'wb' ) as image:
                        shutil.copyfileobj ( file.file, image )
                    url=str ( 'media/' + file.filename )
                    create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                           user=current_user, db=db )
        elif not order.day2:
            db.query ( Orders ).filter ( Orders.id == id ).update ( {
                Orders.id: id,
                Orders.user_id: current_user.id,
                Orders.day2: datetime.datetime.now ( ).date ( ),
            } )
            db.commit ( )
            if files:
                for file in files:
                    with open ( "media/" + file.filename, 'wb' ) as image:
                        shutil.copyfileobj ( file.file, image )
                    url=str ( 'media/' + file.filename )
                    create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                           user=current_user, db=db )
        else:
            db.query ( Orders ).filter ( Orders.id == id ).update ( {
                Orders.id: id,
                Orders.user_id: current_user.id,
                Orders.order_status:order_status,
                Orders.day3: datetime.datetime.now ( ).date ( ),
                Orders.control_date: datetime.datetime.now ( ).date ( ),
            } )

            db.commit ( )
            if files:
                for file in files:
                    with open ( "media/" + file.filename, 'wb' ) as image:
                        shutil.copyfileobj ( file.file, image )
                    url=str ( 'media/' + file.filename )
                    create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                           user=current_user, db=db )

            update_order_status ( order_id=id, user_id=current_user.id, db=db )
    raise HTTPException ( status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi" )





@router_order.delete ( '/delete', status_code=200 )
async def delete_order(id: int = 0, db: Session = Depends ( get_db ), current_user: UserCurrent = Depends (
    get_current_active_user )):  # current_user: User = Depends(get_current_active_user)
    if id:
        return await returned_products ( id, current_user, db )

