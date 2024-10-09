from sqlalchemy.orm import Session

from complaints.models.iikoproducts import IikoProducts


def get_found_products(db: Session, q):
    query = db.query(IikoProducts).filter(q.lower() in IikoProducts.name.lower()).all()
    return query


def get_child_products(db: Session, id):
    query = db.query(IikoProducts).filter(IikoProducts.parentid == id).all()
    return query


def get_product(db:Session,id):
    query = db.query(IikoProducts).filter(IikoProducts.id == id).first()
    return query


def create_product(db:Session,product):
    query = IikoProducts(
        id=product['id'],
        name=product['name'],
        num=product['num'],
        code=product['code'],
        parentid=product['parentid']
    )

    db.add(query)
    db.commit()
    return True


def update_product(db:Session,product):
    query = db.query(IikoProducts).filter(IikoProducts.id == product['id']).first()
    query.name = product['name']
    query.num = product['num']
    query.code = product['code']
    query.parentid = product['parentid']

    db.commit()
    return True


def update_create_products(db:Session, data):

    for product in data:
        is_product_exist = get_product(db, product['id'])
        if is_product_exist:
            update_product(db, product)
        else:
            create_product(db, product)