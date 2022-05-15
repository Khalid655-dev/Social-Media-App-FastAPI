from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db


router = APIRouter(prefix="/admins", tags=["Admins"])


@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.AdminOut)
def create_admin(admin: schemas.AdminSignup, db: Session = Depends(get_db)):

    hashed_password = utils.hash(admin.password)
    admin.password = hashed_password

    new_admin = models.Admin(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


@router.get("/{id}", response_model=schemas.AdminOut)
def get_admin(id: int, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")

    return admin


@router.post("/teacher", status_code= status.HTTP_201_CREATED, response_model=schemas.TeacherOut)
def create_teacher(teacher: schemas.TeacherSignup, db: Session = Depends(get_db), current_admin: int = Depends(oauth2.get_current_admin)):

    hashed_password = utils.hash(teacher.password)
    teacher.password = hashed_password

    new_teacher = models.Teacher(**teacher.dict())
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher