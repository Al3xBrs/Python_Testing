from ..server import loadClubs, loadCompetitions, update_clubs
import json


class TestClub:
    @classmethod
    def create_club(cls):
        club_data = {
            "name": "TEST",
            "email": "test@test.fr",
            "points": "15",
        }

        with open("clubs.json", "r") as c:
            json_data = json.load(c)

        json_data["clubs"].append(club_data)

        with open("clubs.json", "w") as c:
            json.dump(json_data, c, indent=4)

        update_clubs()

    @classmethod
    def delete_club(cls):
        with open("clubs.json", "r") as c:
            json_data = json.load(c)

        new_clubs = [club for club in json_data["clubs"] if club["name"] != "TEST"]
        json_data["clubs"] = new_clubs

        with open("clubs.json", "w") as c:
            json.dump(json_data, c, indent=4)

        update_clubs()


def test_should_load_club_correctly():
    TestClub.create_club()
    expected_club = {
        "name": "TEST",
        "email": "test@test.fr",
        "points": "15",
    }
    clubs = loadClubs()
    test_club = [club for club in clubs if club["name"] == "TEST"]
    assert test_club == [expected_club]
    TestClub.delete_club()


def test_should_load_competition_correctly():
    expected_competition = {
        "name": "Test me !",
        "date": "2023-09-11 12:00:00",
        "numberOfPlaces": "10",
    }
    competitions = loadCompetitions()
    test_competition = [c for c in competitions if c["name"] == "Test me !"]
    assert test_competition == [expected_competition]
