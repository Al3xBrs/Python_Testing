from locust import HttpUser, task, between
import time
from ..tests_unitaires.models import TestClub, TestCompetition


class HttpRequestUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        TestClub.create_club()
        TestCompetition.create_comp()
        self.client.post(
            "/showSummary",
            data={"email": "test@test.fr"},
        )

    @task
    def display_points(self):
        self.client.get("/points_display")

    def on_stop(self):
        self.client.get("/logout")
        TestClub.delete_club()
        TestCompetition.delete_competition()
