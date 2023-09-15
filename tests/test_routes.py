from ..server import (
    update_competitions,
    app,
)

from .models import TestClub, TestCompetition

from flask_testing import TestCase


class TestRoutes(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_should_return_code_ok_index_points_display(self):
        responses = [
            self.client.get("/"),
            self.client.get("/points_display"),
        ]
        for response in responses:
            self.assert200(response)

    def test_should_connect_correct_club_showSummary(self):
        TestClub.create_club()

        try:
            response = self.client.post("/showSummary", data={"email": "test@test.fr"})
            self.assert200(response)
            self.assertIn("test@test.fr", response.get_data(as_text=True))

        finally:
            TestClub.delete_club()

    def test_should_return_correct_competitions_showSummary(self):
        TestClub.create_club()
        TestCompetition.create_comp()

        response = self.client.post(
            "/showSummary",
            data={
                "email": "test@test.fr",
            },
        )

        try:
            self.assert200(response)
            competitions = update_competitions()
            text_response = response.get_data(as_text=True)
            for comp in competitions:
                self.assertIn(f"{comp['name']}", text_response)
                self.assertIn(f"{comp['date']}", text_response)
                self.assertIn(f"{comp['numberOfPlaces']}", text_response)

        finally:
            TestClub.delete_club()
            TestCompetition.delete_competition()

    def test_should_return_correct_name_places_competitions_book(self):
        TestClub.create_club()
        TestCompetition.create_comp()

        response = self.client.get(
            "/book/TEST/TEST",
        )

        try:
            self.assert200(response)
            text_response = response.get_data(as_text=True)
            self.assertIn("TEST", text_response)
            self.assertIn("Places available: 10", text_response)

        finally:
            TestClub.delete_club()
            TestCompetition.delete_competition()
