from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):
    @task
    def filters(self):
        self.client.get("/filters", timeout=120)  # Set a 120-second timeout

    @task
    def tracks(self):
        self.client.get("/tracks?date=2021-01-01&region=United%20States&artist=Shakira", timeout=120)


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    host = "http://127.0.0.1:3000"

