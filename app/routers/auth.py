from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi.applications import FastAPI
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2


router = APIRouter(tags=["Authentication"])

 
@router.post('/login', response_model=schemas.Token)
def login(admin_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    admin = db.query(models.Admin).filter(
        models.Admin.email == admin_credentials.username).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(admin_credentials.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"admin_id": admin.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/login/teacher', response_model=schemas.Token)
def login_teacher(teacher_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    teacher = db.query(models.Teacher).filter(
        models.Teacher.email == teacher_credentials.username).first()

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(teacher_credentials.password, teacher.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"teacher_id": teacher.id})

    return {"access_token": access_token, "token_type": "bearer"}

 
