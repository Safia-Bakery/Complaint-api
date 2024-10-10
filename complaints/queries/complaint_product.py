from sqlalchemy.orm import Session
from complaints.models.complaint_products import ComplaintProducts


def create_complaint_product(db: Session,complaint_id,product_id):
    query = ComplaintProducts(
        complaint_id=complaint_id,
        product_id=product_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query