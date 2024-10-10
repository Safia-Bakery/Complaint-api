from sqlalchemy.orm import Session
from complaints.models.request_model import Files


def create_file(db: Session,complaint_id, url):
    query = Files(
        complaint_id=complaint_id,
        url = url
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query
