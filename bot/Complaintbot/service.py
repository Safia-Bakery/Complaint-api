from datetime import datetime
import requests
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


def send_file_telegram(bot_token, chat_id, file_path, caption=None, reply_to_message_id=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    # 'files' for sending documents is a dictionary with a tuple (optional filename, file data)
    if file_path is None:
        return requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data={"chat_id": chat_id, "text": caption}).json()
    else:

        with open(file_path, 'rb') as file:
            files = {'document': (file_path, file)}
            data = {'chat_id': chat_id,'reply_to_message_id':reply_to_message_id}

            # Make a POST request to the Telegram API
            response = requests.post(url, data=data, files=files)
            print(response.json())
            print(reply_to_message_id)
        return response.json()


    
