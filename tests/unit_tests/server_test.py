import server

server.clubs = [
    {"name": "club-test1", "email": "user-exist@test.fr", "points": "1"}
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
