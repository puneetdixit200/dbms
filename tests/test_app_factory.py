from expense_tracker import create_app


def test_login_page_loads_without_database_connection():
    app = create_app({"TESTING": True, "SECRET_KEY": "test"})

    response = app.test_client().get("/login")

    assert response.status_code == 200
    assert b"Login" in response.data


def test_dashboard_redirects_anonymous_user_to_login():
    app = create_app({"TESTING": True, "SECRET_KEY": "test"})

    response = app.test_client().get("/dashboard")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

