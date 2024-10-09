import requests
from complaints.core.config import BASE_URL, USERNAME, PASSWORD


class ApiRoutes:
    def __init__(self):
        self.base_url = str(BASE_URL)
        self.username = str(USERNAME)
        self.password = str(PASSWORD)
        self.headers = {
            'accept': 'application/json',
            "Authorization": f"Bearer {self.get_token()}"
        }

    def get_token(self):
        url = f"{self.base_url}api/v1/login/"
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'scope': '',
            'client_id': 'string',
            'client_secret': 'string'
        }
        response = requests.post(url=url, headers=headers, data=body).json()

        access_token = response["access_token"]

        return access_token



    def get_all_folders(self):
        response = requests.get(f"{self.base_url}api/v1/folders", headers=self.headers)

        return response.json()

    def get_one_folder(self, id):
        response = requests.get(f"{self.base_url}api/v1/folders/", headers=self.headers, params={"id": id})

        return response.json()

    def get_all_products(self):
        response = requests.get(f"{self.base_url}api/v1/products", headers=self.headers)

        return response.json()

    def get_one_product(self, id):
        response = requests.get(f"{self.base_url}api/v1/folders/", headers=self.headers, params={"id": id})

        return response.json()
