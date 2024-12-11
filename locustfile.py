from locust import HttpUser, task, between

class SpotifyMicroserviceUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def test_filters(self):
        self.client.get("/filters", timeout=30)

    @task
    def test_tracks(self):
        self.client.get("/tracks?date=2021-01-01&region=United States&artist=Shakira&limit=20&offset=0", timeout=30)
