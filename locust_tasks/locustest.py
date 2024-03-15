from locust import HttpUser, task, between
from requests.auth import HTTPBasicAuth
import requests
import random

with open("/locust_tasks/output.txt", "a") as f:
    f.write(f"_________________________________________________\n")

class NextcloudUser(HttpUser):
    auth = None
    user_name = None
    wait_time = between(1, 5)

    def on_start(self):
        user_idx = random.randrange(0, 40)
        self.user_name = f'locust_user{user_idx}'
        self.auth = HTTPBasicAuth(self.user_name, 'test_password1234!')


    def verify_authentication(self):
        response = self.client.head("/remote.php/dav", auth=self.auth)
        if response.status_code != 200:
            with open("/locust_tasks/output.txt", "a") as f:
                f.write(f"Authentication failed for user {self.user_name}: {response.text}.\n")
            raise Exception(f"Authentication failed for user {self.user_name}")

    
    def propfind(self):
        try:
            response = self.client.request("PROPFIND", f"/remote.php/dav/files/{self.user_name}/", auth=self.auth)
            response.raise_for_status()
        except Exception as e:
            with open("/locust_tasks/output.txt", "a") as f:
                f.write(f"Error during PROPFIND request: {e} for user {self.user_name}.\n")


    def read_file_test(self):
        try:
            response = self.client.get(f"/remote.php/dav/files/{self.user_name}/Readme.md", auth=self.auth)
            response.raise_for_status()
        except Exception as e:
            with open("/locust_tasks/output.txt", "a") as f:
                f.write(f"Error during GET request: {e} for user {self.user_name}.\n")

    def upload_file_1kb(self):
        try:
            path = f'/remote.php/dav/files/{self.user_name}/1kb_file_{random.randrange(0, 20)}'
            with open("/test_data/test_1kb", "rb") as f:
                self.client.put(path, data=f, auth=self.auth)
            self.client.delete(path, auth=self.auth)
        except Exception as e:
            with open("/locust_tasks/output.txt", "a") as f:
                f.write(f"Error during PUT request: {e} for user {self.user_name}.\n")

    
    def upload_file_1mb(self):
        try:
            path = f'/remote.php/dav/files/{self.user_name}/1mb_file_{random.randrange(0, 20)}'
            with open("/test_data/test_1mb", "rb") as f:
                self.client.put(path, data=f, auth=self.auth)
            self.client.delete(path, auth=self.auth)
        except Exception as e:
            with open("/locust_tasks/output.txt", "a") as f:
                f.write(f"Error during PUT request: {e} for user {self.user_name}.\n")

    def upload_file_1gb(self):
        try:
            path = f'/remote.php/dav/files/{self.user_name}/1gb_file_{random.randrange(0, 20)}'
            with open("/test_data/test_1gb", "rb") as f:
                self.client.put(path, data=f, auth=self.auth)
            self.client.delete(path, auth=self.auth)
        except Exception as e:
            with open("/locust_tasks/output.txt", "a") as f:
                f.write(f"Error during PUT request: {e} for user {self.user_name}.\n")

    
    @task(1)
    def proper_task(self):
        random_flat = random.random()

        if random_flat < 0.20:
            self.propfind()
        if random_flat < 0.4:
            self.upload_file_1kb()
        elif random_flat < 0.6:
            self.upload_file_1mb()
        elif random_flat < 8:
            self.upload_file_1gb()
        else:
            self.read_file_test()
