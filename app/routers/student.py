from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import oauth2
from .. import models, schemas
from ..database import get_db


router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=List[schemas.StudentOut])
def get_students(db: Session = Depends(get_db), current_admin: int = Depends(oauth2.get_current_admin), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    students = db.query(models.Student).filter(models.Student.subject.contains(search)).limit(limit).offset(skip).all()
    return students


@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Student)
def create_students(student: schemas.StudentCreate, db: Session = Depends(get_db), current_admin: int = Depends(oauth2.get_current_admin)):
    
   ## coursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
   ## new_post = coursor.fetchone()
   ## conn.commit()
     
     new_student = models.Student(admin_id=current_admin.id, **student.dict())
     db.add(new_student)
     db.commit()
     db.refresh(new_student)
     return new_student


@router.get("/{id}", response_model=schemas.StudentOut)
def get_student(id: int, db: Session = Depends(get_db), current_admin: int = Depends(oauth2.get_current_admin)):
   ## coursor.execute("""SELECT * from posts where id = %s """, (str(id)))
    ##post = coursor.fetchone() 
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")

    return student


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_student(id: int, db: Session = Depends(get_db), current_admin: int = Depends(oauth2.get_current_admin)):
    ##coursor.execute("""Delete from posts where id = %s returning *""", (str(id)))
   ## deleted_post = coursor.fetchone()
   ## conn.commit()
    student_query = db.query(models.Student).filter(models.Student.id == id)
    student= student_query.first()
    
    if student_query.first == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with id: {id} is not found")
    
    if student.admin_id != current_admin.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform the requested action")

    student_query.delete(synchronize_session= False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Student)
def update_student(id: int, updated_student: schemas.StudentCreate, db: Session = Depends(get_db), current_admin: int = Depends(oauth2.get_current_admin)):
    ##coursor.execute("""update posts SET title = %s, content = %s, published = %s where id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    ##updated_post = coursor.fetchone()
    ##conn.commit()
    student_query = db.query(models.Student).filter(models.Student.id == id)
    student = student_query.first()

    if student == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")

    if student.admin_id != current_admin.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform the requested action")

    student_query.update(updated_student.dict(), synchronize_session=False)
    
    db.commit() 

    return student_query.first()