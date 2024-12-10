from locust import HttpUser, task, between


class SpotifyMicroserviceUser(HttpUser):
    # Set a wait time between tasks
    wait_time = between(1, 2)

    @task
    def test_rankings(self):
        self.client.get("/rankings?region=United States&date=2021-01-01&limit=10")

    @task
    def test_artist(self):
        self.client.get("/artist?artist=Shakira&limit=5&offset=10")
