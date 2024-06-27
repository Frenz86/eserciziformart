#main.py
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
import models
from database import engine, sessionlocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

class UserUpdate(BaseModel):
    name: str
    position: str
    office: str


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
 
def get_db():
    db = sessionlocal()
    try:
        yield db #using the yield keyword with a database connection allows you to automatically close the connection when you're done with it, even if an error occurs.
    finally:
        db.close()
 
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id.desc())
    return templates.TemplateResponse("index.html", {"request": request, "users": users})
 
@app.post("/add")
async def add(request: Request, name: str = Form(...), position: str = Form(...), office: str = Form(...), db: Session = Depends(get_db)):
    users = models.User(name=name, position=position, office=office)
    db.add(users)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
 
@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})
 
@app.get("/edit/{user_id}")
async def edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "user": user})
 
@app.put("/update/{user_id}")
async def update(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.name = user_update.name
    user.position = user_update.position
    user.office = user_update.office
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.delete("/delete/{user_id}")
async def delete(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
