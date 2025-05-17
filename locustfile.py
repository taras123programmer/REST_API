from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def get_book(self):
        self.client.get("/book")