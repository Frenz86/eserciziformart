# crud/main.py
from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uvicorn
import models
from database import Base, engine, SessionLocal

#########################################################
## Database

Base.metadata.create_all(engine)  

# yield permette di restituire la sessione all'invocatore del contesto. Questo è tipicamente usato nei generatori 
# e nei contesti asincroni per fornire la sessione di database al servizio delle funzioni che lo invocano.
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

class TaskCreate(BaseModel):
    task: str

class Task(BaseModel):
    id: int
    task: str
    
    class Config:
        from_attributes = True

###########################################################

app = FastAPI()

@app.get("/")
async def home():
    return {'localhost:8000/docs'}

###################################################################
@app.post("/todo", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    task_db = models.Task(task=task.task)
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db

@app.get("/todo/all", response_model=List[Task])
def read_all_tasks(session: Session = Depends(get_session)):
    tasks = session.query(models.Task).all()  # Get all tasks
    return tasks

@app.get("/todo/{id}", response_model=Task)
def read_task(id: int, session: Session = Depends(get_session)):
    task = session.query(models.Task).get(id)  # Get item with given id
    # Check if id exists. If not, return 404 not found response
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    return task

@app.put("/todo/{id}", response_model=Task)
def update_task(id: int, task: str, session: Session = Depends(get_session)):
    task_db = session.query(models.Task).get(id)  # Get given id
    if task_db:
        task_db.task = task
        session.commit()
    # Check if id exists. If not, return 404 not found response
    if not task_db:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    return task_db

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, session: Session = Depends(get_session)):
    task_db = session.query(models.Task).get(id)
    # If task with given id exists, delete it from the database. Otherwise, raise 404 error
    if task_db:
        session.delete(task_db)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    return None


###################################################################
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True)