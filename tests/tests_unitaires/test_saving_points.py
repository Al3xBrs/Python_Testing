from ...server import (
    update_clubs,
    update_competitions,
    purchasePlaces,
    points_display,
    app,
)
from .models import TestClub, TestCompetition
from flask_testing import TestCase
from flask import Flask, get_flashed_messages, request


class TestPoints(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_should_return_confirm_message(self):
        TestClub.create_club()
        TestCompetition.create_comp()

        test_club = [c for c in update_clubs() if c["name"] == "TEST"][0]
        test_comp = [comp for comp in update_competitions() if comp["name"] == "TEST"][
            0
        ]

        try:
            with self.app.test_request_context("/purchasePlaces", method="POST"):
                form_data = request.form.to_dict()

                form_data["competition"] = test_comp["name"]
                form_data["club"] = test_club["name"]
                form_data["places"] = "2"

                request.form = form_data
                response = purchasePlaces()

                flashed_messages = list(get_flashed_messages())
                self.assertIn("Great-booking complete!", flashed_messages)
        finally:
            TestClub.delete_club()
            TestCompetition.delete_competition()

    def test_should_save_places(self):
        TestClub.create_club()
        TestCompetition.create_comp()

        test_club = [c for c in update_clubs() if c["name"] == "TEST"][0]
        test_comp = [comp for comp in update_competitions() if comp["name"] == "TEST"][
            0
        ]

        try:
            with self.app.test_request_context("/purchasePlaces", method="POST"):
                form_data = request.form.to_dict()

                form_data["competition"] = test_comp["name"]
                form_data["club"] = test_club["name"]
                form_data["places"] = "2"

                request.form = form_data
                response = purchasePlaces()

            self.assertIn(f"{test_comp['name']}", response)
            self.assertIn(f"{test_comp['date']}", response)
            self.assertIn(f"{test_comp['numberOfPlaces']}", response)

        finally:
            TestClub.delete_club()
            TestCompetition.delete_competition()

    def test_should_save_points(self):
        TestClub.create_club()
        TestCompetition.create_comp()

        test_club = [c for c in update_clubs() if c["name"] == "TEST"][0]
        test_comp = [comp for comp in update_competitions() if comp["name"] == "TEST"][
            0
        ]

        try:
            with self.app.test_request_context("/purchasePlaces", method="POST"):
                form_data = request.form.to_dict()

                form_data["competition"] = test_comp["name"]
                form_data["club"] = test_club["name"]
                form_data["places"] = "2"
                points = int(test_club["points"]) - int(form_data["places"])
                request.form = form_data
                response = purchasePlaces()

            self.assertIn(f"Points available: {points}", response)

        finally:
            TestClub.delete_club()
            TestCompetition.delete_competition()
