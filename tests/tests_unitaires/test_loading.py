from ...server import loadClubs, loadCompetitions
from .models import TestClub, TestCompetition


def test_should_load_club_correctly():
    TestClub.create_club()
    expected_club = {
        "name": "TEST",
        "email": "test@test.fr",
        "points": "15",
    }
    clubs = loadClubs()
    test_club = [club for club in clubs if club["name"] == "TEST"]

    try:
        assert test_club == [expected_club]

    finally:
        TestClub.delete_club()


def test_should_load_competition_correctly():
    TestCompetition.create_comp()

    expected_competition = {
        "name": "TEST",
        "date": "2023-09-15 12:00:00",
        "numberOfPlaces": "10",
    }
    competitions = loadCompetitions()
    test_competition = [c for c in competitions if c["name"] == "TEST"]

    try:
        assert test_competition == [expected_competition]

    finally:
        TestCompetition.delete_competition()
