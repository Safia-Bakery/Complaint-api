from sqlalchemy.orm import Session
from complaints.models.iikofolders import IikoFolders





def get_found_folders(db: Session, name, parent_id):
    query = db.query(IikoFolders)
    if name is None and parent_id is None:
        query  = query.filter(IikoFolders.parent_id.is_(None))
    else:
        if name:
            query = query.filter(IikoFolders.name.ilike(f"%{name}%"))
        if parent_id:
            query = query.filter(IikoFolders.parent_id == parent_id)
    return query.all()





def get_folder(db:Session,id):
    query = db.query(IikoFolders).filter(IikoFolders.id == id).first()
    return query


def create_folder(db:Session,folder):
    query = IikoFolders(
        id=folder['id'],
        num=folder['num'],
        code=folder['code'],
        name=folder['name'],
        parent_id=folder['parent'],
        category=folder['category'],
        description=folder['description']
    )

    db.add(query)
    db.commit()
    return True


def update_folder(db:Session,folder):
    query = db.query(IikoFolders).filter(IikoFolders.id == folder['id']).first()
    query.num = folder['num']
    query.code = folder['code']
    query.name = folder['name']
    query.parent_id = folder['parent']
    query.category = folder['category']
    query.description = folder['description']

    db.commit()
    return True


def update_create_folders(db:Session, data):

    for folder in data:
        is_folder_exist = get_folder(db, folder['id'])
        if is_folder_exist:
            update_folder(db, folder)
        else:
            create_folder(db, folder)

    return True
