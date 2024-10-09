import requests
from core.config import BASE_URL, USERNAME, PASSWORD


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
        url = f"{self.base_url}/login"
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        print("username: ", self.username)
        print("password: ", self.password)
        body = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'scope': '',
            'client_id': 'string',
            'client_secret': 'string'
        }
        response = requests.post(url=url, headers=headers, data=body).json()
        print("creating token, response: ", response)

        access_token = response["access_token"]
        # refresh_token = response["refresh_token"]

        return access_token

    # def get_user(self, user_id):
    #     response = requests.get(f"{self.base_url}/kru_users/", headers=self.headers, params={'telegram_id': user_id})
    #     return response.json()
    #
    # def edit_user(self, user_name, branch_id, user_id):
    #     body = {
    #         "full_name": user_name,
    #         "branch_id": branch_id,
    #         "id": user_id
    #     }
    #     response = requests.put(f"{self.base_url}/kru_users/", headers=self.headers, json=body)
    #     return response.json()
    #
    # def create_user(self, tg_id, user_name, branch_id):
    #     body = {
    #         "full_name": user_name,
    #         "telegram_id": tg_id,
    #         "branch_id": branch_id
    #     }
    #     response = requests.post(f"{self.base_url}/kru_users/", headers=self.headers, data=body)
    #     return response.json()

    # def get_all_branches(self):
    #     params = {
    #         'page': 1,
    #         'size': 100
    #     }
    #     response = requests.get(f"{self.base_url}/branchs/", headers=self.headers, params=params).json()
    #     branch_list = [branch["name"] for branch in response["items"]]
    #     pages = response["pages"]
    #     page = response["page"]
    #     for i in range(page, pages + 1):
    #         # print("i: ", i)
    #         response = requests.get(f"{self.base_url}/branchs/", headers=self.headers,
    #                                 params={'page': i, 'size': 100}).json()
    #         branch_list.extend([branch["name"] for branch in response["items"]])
    #
    #     # print("BRANCHES: ", len(branch_list))
    #     return branch_list

    def get_all_folders(self):
        response = requests.get(f"{self.base_url}/folders", headers=self.headers)

        return response.json()

    def get_one_folder(self, id):
        response = requests.get(f"{self.base_url}/folders/", headers=self.headers, params={"id": id})

        return response.json()

    def get_all_products(self):
        response = requests.get(f"{self.base_url}/products", headers=self.headers)

        return response.json()

    def get_one_product(self, id):
        response = requests.get(f"{self.base_url}/folders/", headers=self.headers, params={"id": id})

        return response.json()
