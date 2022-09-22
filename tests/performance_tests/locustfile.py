from locust import HttpUser, task


class GudlftPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task
    def book(self):
        self.client.get("/book/Fall Classic/She Lifts")

    @task
    def show_summary(self):
        self.client.post("/show_summary", data={"email": "kate@shelifts.co.uk"})

    @task
    def purchase(self):
        self.client.post(
            "/purchase_places",
            data={
                "competition": "Fall Classic",
                "club": "She Lifts",
                "places": 2,
            },
        )

    @task
    def display_clubs(self):
        self.client.get("/display_clubs")

    @task
    def logout(self):
        self.client.get("/logout")
