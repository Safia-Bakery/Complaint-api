from database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def transform_list(lst, size, key, lang):
    # if key=='id':
    
    #     return [[f"{item.id}" for item in lst[i:i+size]] for i in range(0, len(lst), size)]
    if key=='name':
        return [[f"{item.name}" if lang == 'ru' else f"{item.name_uz}" for item in lst[i:i+size]] for i in range(0, len(lst), size)]