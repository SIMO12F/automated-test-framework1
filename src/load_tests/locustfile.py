from locust import HttpUser, task, between

class PythonOrgUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index_page(self):
        self.client.get("/")

    @task(3)
    def view_docs(self):
        self.client.get("/doc/")

    @task(2)
    def search_python(self):
        self.client.get("/search/?q=python")