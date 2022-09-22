import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [
            club for club in clubs if club["email"] == request.form["email"]
        ][0]
        return render_template(
            "welcome.html", club=club, competitions=competitions
        )
    except IndexError:
        if request.form["email"] != "":
            flash("Email not in database !")
        else:
            flash("You cannot leave this field empty !")
        return render_template("index.html")


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", club=club, competitions=competitions
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [
        c for c in competitions if c["name"] == request.form["competition"]
    ][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = request.form["places"]
    if placesRequired == "":
        flash("You must type a number !")
    else:
        placesRequired = int(request.form["places"])
        competition_time = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")

        # add name competition + places booked in value, in club dict.
        if competition["name"] not in club:
            club[competition["name"]] = int(0)

        if datetime.now() < competition_time:
            if placesRequired <= 0:
                flash("You cannot reserve 0 places or negative number !")
            else:
                if placesRequired + club[competition["name"]] < 13:
                    if placesRequired <= int(
                        competition["numberOfPlaces"]
                    ) and placesRequired <= int(club["points"]):
                        competition["numberOfPlaces"] = (
                            int(competition["numberOfPlaces"]) - placesRequired
                        )
                        club[competition["name"]] = (
                            int(club[competition["name"]]) + placesRequired
                        )
                        flash("Great-booking complete!")
                    elif placesRequired > int(club["points"]):
                        flash("You cannot reserve more places than you have")
                    elif int(club["points"]) > int(
                        competition["numberOfPlaces"]
                    ):
                        flash(
                            f"Problem, the competition only has {int(competition['numberOfPlaces'])} places, you ask for {placesRequired}"
                        )
                    else:
                        flash("There was a problem, please try again")
                else:
                    flash("No more than 12 places per competition !")
        else:
            flash(
                "You cannot book this competition, because it has already taken place."
            )
    return render_template(
        "welcome.html", club=club, competitions=competitions
    )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
