import server

server.clubs = [
    {"name": "club-test1", "email": "user-exist@test.fr", "points": "1"},
    {"name": "club-test2", "email": "user-exist2@test.fr", "points": "7"},
]

server.competitions = [
    {
        "name": "Competition-test1",
        "date": "2023-02-07 00:00:00",
        "numberOfPlaces": "15",
    },
    {
        "name": "Competition-test2",
        "date": "2030-12-12 00:00:00",
        "numberOfPlaces": "5",
    },
]
"""
TESTS FOR : Error/'Entering a unknown email crashes the app' & logout :
"""


def test_mail_in_db(client):
    response = client.post(
        "/showSummary", data={"email": "user-exist@test.fr"}
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
