import json
from flask import Flask, render_template, request, redirect, flash, url_for
import logging
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def update_clubs():
    global clubs
    clubs = loadClubs()
    return clubs


def update_competitions():
    global competitions
    competitions = loadCompetitions()
    return competitions


def write_json_clubs(clubs):
    with open("clubs.json", "r") as file:
        data = json.load(file)

    data.update({"clubs": clubs})

    with open("clubs.json", "w") as file:
        json.dump(data, file, indent=4)


def write_json_competitions(competitions):
    with open("competitions.json", "r") as file:
        data = json.load(file)

    data.update({"competitions": competitions})

    with open("competitions.json", "w") as file:
        json.dump(data, file, indent=4)


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    dnow = datetime.now()
    futur_competitions = [
        competition
        for competition in competitions
        if datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") > dnow
    ]
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]

        return render_template(
            "welcome.html", club=club, competitions=futur_competitions
        )

    except:
        flash("This email DOES NOT exist. Try again.")
        return render_template("index.html")


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    foundClub["points"] = int(foundClub["points"])
    max_points = min(
        [int(foundCompetition["numberOfPlaces"]), int(foundClub["points"]), 12]
    )
    print(max_points)
    if foundClub and foundCompetition:
        return render_template(
            "booking.html",
            club=foundClub,
            competition=foundCompetition,
            max_points=max_points,
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]

    club = [c for c in clubs if c["name"] == request.form["club"]][0]

    placesRequired = int(request.form["places"])

    if placesRequired <= 12:
        if placesRequired <= int(club["points"]):
            competition["numberOfPlaces"] = str(
                int(competition["numberOfPlaces"]) - placesRequired
            )
            club["points"] = str(int(club["points"]) - placesRequired)
        else:
            logging.warning("You DO NOT have enough points.")
            flash("You DO NOT have enough points.")
            return render_template("booking.html", club=club, competition=competition)
    else:
        logging.warning("You DO NOT have permission to purchase more than 12 places.")
        flash("You DO NOT have permission to purchase more than 12 places.")
        return render_template("booking.html", club=club, competition=competition)

    flash("Great-booking complete!")
    write_json_clubs(clubs)
    write_json_competitions(competitions)

    dnow = datetime.now()
    futur_competitions = [
        competition
        for competition in competitions
        if datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") > dnow
    ]
    return render_template("welcome.html", club=club, competitions=futur_competitions)


@app.route("/points_display")
def points_display():
    clubs_points_list = [[club["name"], int(club["points"])] for club in clubs]
    return render_template("points_display.html", clubs_points_list=clubs_points_list)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    update_competitions()
    update_clubs()
    app.run(debug=True)
