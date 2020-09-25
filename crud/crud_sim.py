from sqlalchemy.orm import Session

from models import sim,message
from schemas import sim_schema

def get_sim(db: Session,tty_gateway:str):
    return db.query(sim.Sim).filter(sim.Sim.tty_gateway == tty_gateway).first()


def get_all_sim(db: Session):
    return db.query(sim.Sim).all()

def get_sim_by_number(db: Session, sim_number: str):
    return db.query(sim.Sim).filter(sim.Sim.sim_number ==sim_number ).first()



def get_message(db:Session,sim_number:str):
    return db.query(message.Message).filter(message.Message.phone_owner==sim_number).all()

def get_all_message(db:Session):
    return db.query(message.Message).all()

def count_shop(db:Session,sim_number:str):
    return db.query(message.Message).filter(message.Message.phone_owner==sim_number).count()