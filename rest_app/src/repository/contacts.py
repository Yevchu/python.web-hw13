from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactModel

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

async def get_contact_by_first_name(contact_first_name: str, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.first_name == contact_first_name, Contact.user_id == user.id)).first()

async def get_contact_by_last_name(contact_last_name: str, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.last_name == contact_last_name, Contact.user_id == user.id)).first()

async def get_contact_by_email(contact_email: str, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.email == contact_email, Contact.user_id == user.id)).first()

async def upcoming_birthday(user: User, db: Session) -> List[Contact]:
    today = datetime.today().date()
    end_date = today + timedelta(days=7)
    return db.query(Contact).filter(and_(Contact.birthday >= today, Contact.birthday <= end_date, Contact.user_id == user.id)).all()

async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        birthday=body.birthday,
        description=body.description,
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact

async def delete_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact