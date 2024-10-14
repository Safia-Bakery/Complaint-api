from sqlalchemy.orm import Session
from complaints.models.request_model import Branchs



def get_branchs(db:Session,id):
    return db.query(Branchs).filter(Branchs.id == id).first()