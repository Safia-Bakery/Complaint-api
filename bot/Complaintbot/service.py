from datetime import datetime

def transform_list(lst, size, key):
    # if key=='id':
    
    #     return [[f"{item.id}" for item in lst[i:i+size]] for i in range(0, len(lst), size)]
    if key=='name':
        return [[f"{item.name}" for item in lst[i:i+size]] for i in range(0, len(lst), size)]
    


def validate_date(date_string):
    try:
        # Attempt to parse the date string according to the specified format
        datetime.strptime(date_string, "%d.%m.%Y %H:%M")
        return True  # The date is in the correct format
    except ValueError:
        return False
    


def validate_only_date(date_string):
    try:
        # Attempt to parse the date string according to the specified format
        datetime.strptime(date_string, "%d.%m.%Y")
        return True  # The date is in the correct format
    except ValueError:
        return False
    
    
