from flask_testing import TestCase
from ...server import (
    app,
    update_clubs,
    update_competitions,
    purchasePlaces,
    write_json_clubs,
)
from ..tests_unitaires.models import TestClub, TestCompetition
from flask import request, get_flashed_messages


class TestUX(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_full_user_experience(self):
        response = self.client.get("/")
        self.assert200(response)

        TestClub.create_club()
        TestCompetition.create_comp()

        test_club = [c for c in update_clubs() if c["name"] == "TEST"][0]
        test_comp = [comp for comp in update_competitions() if comp["name"] == "TEST"][
            0
        ]
        try:
            response = self.client.post(
                "/showSummary",
                data={"email": "test@test.fr"},
            )
            self.assert200(response)
            self.assertIn("test@test.fr", response.get_data(as_text=True))

            response = self.client.get("/book/TEST/TEST")
            self.assert200(response)
            text_response = response.get_data(as_text=True)
            self.assertIn("TEST", text_response)
            self.assertIn("Places available: 10", text_response)

            with self.app.test_request_context("/purchasePlaces", method="POST"):
                form_data = request.form.to_dict()

                form_data["competition"] = test_comp["name"]
                form_data["club"] = test_club["name"]
                form_data["places"] = "2"

                points = int(test_club["points"]) - int(form_data["places"])

                request.form = form_data
                response = purchasePlaces()

                flashed_messages = list(get_flashed_messages())
                self.assertIn("Great-booking complete!", flashed_messages)

                self.assertIn(f"{test_comp['name']}", response)
                self.assertIn(f"{test_comp['date']}", response)
                self.assertIn(f"{test_comp['numberOfPlaces']}", response)

                self.assertIn(f"Points available: {points}", response)

            TestClub.create_club_0()

            response = self.client.get("book/TEST/TEST0")
            self.assertIn(
                "You DO NOT have enough points.", response.get_data(as_text=True)
            )

        finally:
            TestClub.delete_club()
            TestCompetition.delete_competition()
