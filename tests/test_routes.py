from ..server import (
    index,
    showSummary,
    book,
    purchasePlaces,
    points_display,
    logout,
    loadClubs,
    loadCompetitions,
    app,
)

from .test_loading import TestClub
from flask import Flask
from flask_testing import TestCase

import asyncio


class TestRoutes(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_should_return_code_ok(self):
        responses = [
            self.client.get("/"),
            self.client.get("/points_display"),
        ]
        for response in responses:
            self.assert200(response)

    def test_should_connect_correct_club(self):
        TestClub.create_club()
        response = self.client.post("/showSummary", data={"email": "test@test.fr"})
        self.assert200(response)
        self.assertIn("test@test.fr", response.get_data(as_text=True))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather())
        TestClub.delete_club()

    def test_should_return_correct_competitions(self):
        TestClub.create_club()
        response = self.client.post(
            "/showSummary",
            data={
                "email": "test@test.fr",
            },
        )
        self.assert200(response)
        competitions = loadCompetitions()
        for comp in competitions:
            self.assertIn(f"{comp['name']}", response.get_data(as_text=True))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather())
        TestClub.delete_club()
