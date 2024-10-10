from sqlalchemy.orm import Session
from complaints.models.request_model import Clients


def  get_clients(db: Session,telegram_id: int):
    return db.query(Clients).filter(Clients.id == telegram_id).first()

