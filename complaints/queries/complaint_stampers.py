from sqlalchemy.orm import Session
from complaints.models.complaint_stampers import ComplaintStampers



def create_complaint_stampers(db:Session,complaint_id, user_id):
    query = ComplaintStampers(
        complaint_id=complaint_id,
        user_id=user_id
    )
    db.add(query)
    db.commit()
    return query


def delete_complaint_stampers(db:Session,complaint_id, user_id):
    query = db.query(ComplaintStampers).filter(ComplaintStampers.complaint_id==complaint_id,ComplaintStampers.user_id==user_id).first()
    if query is not None:
        db.delete(query)
        db.commit()
    return query