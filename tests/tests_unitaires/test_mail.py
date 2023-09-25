from flask_testing import TestCase
from ...server import app


class TestMailCheck(TestCase):
    """ """

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_should_display_error_message(self):
        wrong_mail = "blabla@blabla.fr"
        error_message = "This email DOES NOT exist. Try again."

        response = self.client.post(
            "/showSummary",
            data={"email": wrong_mail},
        )

        self.assert200(response)
        self.assertIn(error_message, response.get_data(as_text=True))
