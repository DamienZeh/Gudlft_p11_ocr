import server


"""
TESTS FOR : Error/'Entering a unknown email crashes the app' & logout :
"""


def test_mail_in_db(client):
    response = client.post(
        "/showSummary", data={"email": "user-exist@test.fr"}
    )
    assert "Welcome, user-exist@test.fr" in str(response.data.decode())
    assert not "You cannot leave this field empty !" in str(
        response.data.decode()
    )
    assert not "Email not in database !" in str(response.data.decode())
    assert response.status_code == 200


def test_mail_not_in_db(client):
    response = client.post(
        "/showSummary", data={"email": "wrongmailtest@test.fr"}
    )
    assert "Email not in database !" in str(response.data.decode())
    assert response.status_code == 200


def test_mail_empty(client):
    response = client.post("/showSummary", data={"email": ""})
    assert "You cannot leave this field empty !" in str(response.data.decode())
    assert response.status_code == 200


def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302


"""
TESTS FOR : Bug/'Clubs should not be able to use more than their points allowed' :
"""


def test_purchase_great_booking(client):
    competitions = server.competitions[0]
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test1",
            "competition": "Competition-test1",
            "places": "1",
        },
    )
    assert competitions["numberOfPlaces"] == 14
    assert "Great-booking complete!" in str(response.data.decode())
    assert response.status_code == 200


def test_purchase_with_blank_field_per_competition(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test1",
            "competition": "Competition-test2",
            "places": "",
        },
    )
    assert "You must type a number !" in str(response.data.decode())
    assert response.status_code == 200


def test_purchase_too_points_entered_per_club(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test1",
            "competition": "Competition-test1",
            "places": "2",
        },
    )
    assert "You cannot reserve more places than you have" in str(
        response.data.decode()
    )
    assert response.status_code == 200


def test_purchase_too_points_entered_per_competition(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test2",
            "competition": "Competition-test2",
            "places": "7",
        },
    )
    assert str.encode(f"Number of Places: 5") in response.data
    assert "Problem, the competition only has 5 places, you ask for 7" in str(
        response.data.decode()
    )
    assert response.status_code == 200


def test_purchase_with_zero_point_per_competition(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test2",
            "competition": "Competition-test2",
            "places": "0",
        },
    )
    assert "You cannot reserve 0 places or negative number !" in str(
        response.data.decode()
    )
    assert response.status_code == 200


def test_purchase_with_negative_point_per_competition(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test2",
            "competition": "Competition-test2",
            "places": "-2",
        },
    )
    assert "You cannot reserve 0 places or negative number !" in str(
        response.data.decode()
    )
    assert response.status_code == 200


"""
TESTS FOR : Bug/'Clubs can't be able to book more than 12 places per competition' :
"""


def test_purchase_with_twelve_points_ok(client):
    competitions = server.competitions[4]
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test4",
            "competition": "Competition-test5",
            "places": "12",
        },
    )
    assert "Great-booking complete!" in str(response.data.decode())
    assert competitions["numberOfPlaces"] == 0
    assert response.status_code == 200


def test_purchase_with_too_much_points_per_competition(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test3",
            "competition": "Competition-test2",
            "places": "13",
        },
    )
    assert "No more than 12 places per competition !" in str(
        response.data.decode()
    )
    assert response.status_code == 200


def test_purchase_with_too_much_points_accumulate_per_competition(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test3",
            "competition": "Competition-test4",
            "places": "3",
        },
    )
    assert response.status_code == 200
    response_second = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test3",
            "competition": "Competition-test4",
            "places": "10",
        },
    )
    assert "No more than 12 places per competition !" in str(
        response_second.data.decode()
    )


"""
TESTS FOR : Bug/'Booking places in past competitions' :
"""


def test_purchase_with_good_date(client):
    competitions = server.competitions[1]
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test3",
            "competition": "Competition-test2",
            "date": "2030-12-12 00:00:00",
            "places": "1",
        },
    )
    assert competitions["numberOfPlaces"] == 4
    assert "Great-booking complete!" in str(response.data.decode())
    assert response.status_code == 200


def test_purchase_with_bad_date(client):
    competitions = server.competitions[2]
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test2",
            "competition": "Competition-test3",
            "date": "2019-10-02 00:00:00",
            "places": "1",
        },
    )
    assert competitions["numberOfPlaces"] == "7"
    assert (
        "You cannot book this competition, because it has already taken place."
        in str(response.data.decode())
    )
    assert response.status_code == 200


"""
TESTS FOR : Bug/'points_updates_are_not_reflected' :
"""


def test_purchase_points_club_update(client):
    clubs = server.clubs[4]
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test5",
            "competition": "Competition-test4",
            "date": "2019-10-02 00:00:00",
            "places": "1",
        },
    )

    assert "Great-booking complete!" in str(response.data.decode())
    assert clubs["points"] == 0
    assert response.status_code == 200


"""
TESTS FOR : Feature/'implement_points_display_board' :
"""


def test_page_display_clubs_and_points(client):
    response = client.get("/display_clubs")
    assert response.status_code == 200


def test_display_clubs(client):
    response = client.get("/display_clubs")
    assert "club-test1" in str(response.data)
    assert "club-test2" in str(response.data)


def test_presence_link_to_index(client):
    response = client.get("/display_clubs")
    assert "Retour à l'accueil" in str(response.data.decode())
