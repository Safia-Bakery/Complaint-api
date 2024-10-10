from sqlalchemy.orm import Session

from complaints.models.iikoproducts import IikoProducts





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


def get_iiko_products_by_parent_id(db: Session, parent_id,name):
    query = db.query(IikoProducts)
    if parent_id is not None:
        query = query.filter(IikoProducts.parentid == parent_id)
    if name is not None:
        query = query.filter(IikoProducts.name.ilike(f"%{name}%"))

    return query.all()