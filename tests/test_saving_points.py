from ..server import (
    update_clubs,
    update_competitions,
    purchasePlaces,
    points_display,
    app,
)
from flask_testing import TestCase


class TestPoints(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app
