from database import SessionLocal, Base


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def transform_list(lst, size, key):
    # if key=='id':
    
    #     return [[f"{item.id}" for item in lst[i:i+size]] for i in range(0, len(lst), size)]
    if key=='name':
        return [[f"{item.name}" for item in lst[i:i+size]] for i in range(0, len(lst), size)]