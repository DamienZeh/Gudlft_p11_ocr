import server


"""
TESTS INTEGRATION :
"""


def test_login_and_logout(client):
    response = client.post(
        "/showSummary", data={"email": "user-exist6@test.fr"}
    )
    assert "Welcome, user-exist6@test.fr" in str(response.data.decode())
    assert response.status_code == 200
    response = client.get("/logout")
    assert response.status_code == 302


def test_login_and_purchase(client):
    response = client.post(
        "/showSummary", data={"email": "user-exist6@test.fr"}
    )
    assert "Welcome, user-exist6@test.fr" in str(response.data.decode())
    assert response.status_code == 200
    competitions = server.competitions[5]
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "club-test6",
            "competition": "Competition-test6",
            "places": "1",
        },
    )
    assert competitions["numberOfPlaces"] == 11
    assert "Great-booking complete!" in str(response.data.decode())
    assert response.status_code == 200
