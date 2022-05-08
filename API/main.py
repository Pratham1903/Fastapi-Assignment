
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Menu(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    price: int = Field(gt=-1, lt=101)


MENU = []


@app.get("//retrieve_all_menu_details'")
def all_menu(db: Session = Depends(get_db)):
    return db.query(models.Menu).all()


@app.post("//add_new_menu'")
def create_menu(menu: Menu, db: Session = Depends(get_db)):

    menu_model = models.Menu()
    menu_model.name = menu.name
    menu_model.description = menu.description
    menu_model.price = menu.price

    db.add(menu_model)
    db.commit()

    return menu


@app.put("//update_menu_details'")
def update_menu(menu_id: int, menu: Menu, db: Session = Depends(get_db)):

    menu_model = db.query(models.Menu).filter(models.Menu.id == menu_id).first()

    if menu_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {menu_id} : Does not exist"
        )

    menu_model.name = menu.name
    menu_model.description = menu.description
    menu_model.price = menu.price

    db.add(menu_model)
    db.commit()

    return menu


@app.delete("/delete_menu_by_id")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):

    menu_model = db.query(models.Menu).filter(models.Menu.id == menu_id).first()

    if menu_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {menu_id} : Does not exist"
        )

    db.query(models.Menu).filter(models.Menu.id == menu_id).delete()

    db.commit()

@app.get('/Search')
def get_menu_by_menu_name(menu_name: str,db: Session = Depends(get_db),):
    return db.query(models.Menu).filter(models.Menu.name == menu_name).first()

    

























