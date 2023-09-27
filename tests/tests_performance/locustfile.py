from locust import HttpUser, task, between


class HttpRequestUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.client.post(
            "/showSummary",
            data={"email": "kate@shelifts.co.uk"},
        )

    @task
    def display_points(self):
        self.client.get("/points_display")

    @task
    def book_requests(self):
        self.client.get("book/Spring Festival/She Lifts")
        self.client.get("book/Fall Classic/She Lifts")

    def on_stop(self):
        self.client.get("/logout")
