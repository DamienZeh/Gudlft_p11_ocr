import server


"""
TESTS FONCTIONNELS :
"""


def test_fonctionnal(client):
    """
    It's a test that allows you to login, and reserve places,
        until you take too many. Then we disconnect
    """
    competitions = server.competitions[6]
    clubs = server.clubs[6]
    response = client.post(
        "/show_summary", data={"email": "user-exist7@test.fr"}
    )
    assert "Welcome, user-exist7@test.fr" in str(response.data.decode())
    assert response.status_code == 200

    response = client.post(
        "/purchase_places",
        data={
            "club": "club-test7",
            "competition": "Competition-test7",
            "points": "0",
            "places": "1",
        },
    )
    assert clubs["points"] == 12
    assert competitions["number_of_places"] == 3
    assert "Great-booking complete!" in str(response.data.decode())
    assert response.status_code == 200

    response = client.post(
        "/purchase_places",
        data={
            "club": "club-test7",
            "competition": "Competition-test7",
            "places": "2",
        },
    )
    assert clubs["points"] == 6
    assert competitions["number_of_places"] == 1
    assert "Great-booking complete!" in str(response.data.decode())
    assert response.status_code == 200

    response = client.post(
        "/purchase_places",
        data={
            "club": "club-test7",
            "competition": "Competition-test7",
            "places": "2",
        },
    )
    assert (
        "Problem, the competition only has \
                                1\
                                 places, you ask for 2"
        in str(response.data.decode())
    )
    assert clubs["points"] == 6
    assert competitions["number_of_places"] == 1

    response = client.get("/display_clubs")
    assert "club-test7" in str(response.data)
    assert "2" in str(response.data)

    response = client.get("/logout")
    assert response.status_code == 302
