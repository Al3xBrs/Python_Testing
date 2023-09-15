import json
from ..server import update_clubs, update_competitions


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


class TestCompetition:
    @classmethod
    def create_comp(cls):
        competition = {
            "name": "TEST",
            "date": "2023-09-15 12:00:00",
            "numberOfPlaces": "10",
        }
        with open("competitions.json", "r") as comps:
            json_data = json.load(comps)

        json_data["competitions"].append(competition)

        with open("competitions.json", "w") as comps:
            json.dump(json_data, comps, indent=4)

        update_competitions()

    @classmethod
    def delete_competition(cls):
        with open("competitions.json", "r") as comps:
            json_data = json.load(comps)

        new_comps = [
            comp for comp in json_data["competitions"] if comp["name"] != "TEST"
        ]
        json_data["competitions"] = new_comps

        with open("competitions.json", "w") as comps:
            json.dump(json_data, comps, indent=4)

        update_competitions()
