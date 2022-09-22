import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary():
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
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [c for c in competitions if c["name"] == competition][
        0
    ]
    if found_club and found_competition:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", club=club, competitions=competitions
        )


@app.route("/purchase_places", methods=["POST"])
def purchase_places():
    point_per_place = 3
    competition = [
        c for c in competitions if c["name"] == request.form["competition"]
    ][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]

    places_required = request.form["places"]
    if places_required == "":
        flash("You must type a number !")
    else:
        places_required = int(request.form["places"])

        competition_time = datetime.strptime(
            competition["date"], "%Y-%m-%d %H:%M:%S"
        )

        # add name competition + places booked in value, in club dict.
        if competition["name"] not in club:
            club[competition["name"]] = int(0)

        if datetime.now() < competition_time:
            if places_required <= 0:
                flash("You cannot reserve 0 places or negative number !")
            else:
                if places_required + club[competition["name"]] < 13:
                    if places_required <= int(
                        competition["number_of_places"]
                    ) and places_required * point_per_place <= int(
                        club["points"]
                    ):
                        competition["number_of_places"] = (
                            int(competition["number_of_places"])
                            - places_required
                        )
                        club[competition["name"]] = (
                            int(club[competition["name"]]) + places_required
                        )
                        club["points"] = int(club["points"]) - (
                            places_required * point_per_place
                        )
                        flash("Great-booking complete!")
                    elif places_required * point_per_place > int(
                        club["points"]
                    ):
                        flash("You cannot reserve more places than you have")
                    elif int(club["points"]) > int(
                        competition["number_of_places"]
                    ):
                        flash(
                            f"Problem, the competition only has \
                                {int(competition['number_of_places'])}\
                                 places, you ask for {places_required}"
                        )
                    else:
                        flash("There was a problem, please try again")
                else:
                    flash("No more than 12 places per competition !")
        else:
            flash(
                "You cannot book this competition,\
                     because it has already taken place."
            )

    return render_template(
        "welcome.html", club=club, competitions=competitions
    )


@app.route("/display_clubs")
def show_clubs():
    return render_template("display_clubs.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
