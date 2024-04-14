if __name__ == "__test__":
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)

    def test_register():
        response = client.post(
            "/register",
            json={"id": 1, "username": "test", "email": "test@test.com", "age": 30, "name": "Test User",
                  "password": "test", "phone": "1234567890", "is_admin": False},
        )
        assert response.status_code == 200
        assert response.json() == {"msg": "User registered successfully"}

    def test_login():
        response = client.post(
            "/login",
            data={"username": "test", "password": "test"},
        )
        assert response.status_code == 200
        assert response.json() == {"msg": "Logged in successfully"}

    def test_search_office():
        response = client.post(
            "/search-office",
            json={"parameters": {"name": "Office1"}},
        )
        assert response.status_code == 200

    def test_fill_application():
        response = client.post(
            "/fill-application",
            json={"user_id": 1, "office_id": 1},
        )
        assert response.status_code == 200

    def test_submit_application():
        response = client.post(
            "/submit-application",
            json={"application_id": 1},
        )
        assert response.status_code == 200
        assert response.json() == {"status": "Application submitted"}

    def test_ask_question():
        response = client.post(
            "/ask-question",
            data={"question": "what is the weather today?"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "answer": "I'm sorry, I cannot provide real-time data as my training only includes knowledge up until 2021."}

    def test_add_to_wishlist():
        response = client.post(
            "/add-to-wishlist",
            json={"user_id": 1, "office_id": 1},
        )
        assert response.status_code == 200
        assert response.json() == {"msg": "Office added to wishlist"}

    def test_manage_applications():
        response = client.post(
            "/manage-applications",
            json={"admin_id": 1},
        )
        assert response.status_code == 200

    def test_manage_offices():
        response = client.post(
            "/manage-offices",
            json={"admin_id": 1},
        )
        assert response.status_code == 200

    def test_manage_users():
        response = client.post(
            "/manage-users",
            json={"admin_id": 1},
        )
        assert response.status_code == 200

    def test_generate_report():
        response = client.post(
            "/generate-report",
            json={"admin_id": 1},
        )
        assert response.status_code == 200

    def test_export_report():
        response = client.post(
            "/export-report",
            json={"admin_id": 1},
        )
        assert response.status_code == 200
    def test_register_existing_user():
        response = client.post(
            "/register",
            json={"id": 1, "username": "test", "email": "test@test.com", "age": 30, "name": "Test User",
                  "password": "test", "phone": "1234567890", "is_admin": False},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Username already exists"}

    def test_login_invalid_credentials():
        response = client.post(
            "/login",
            data={"username": "invalid", "password": "invalid"},
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid credentials"}

    def test_search_office_not_found():
        response = client.post(
            "/search-office",
            json={"parameters": {"name": "NonexistentOffice"}},
        )
        assert response.status_code == 200
        assert response.json() == {"offices": []}

    def test_fill_application_invalid_user_or_office():
        response = client.post(
            "/fill-application",
            json={"user_id": 999, "office_id": 999},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "User or office not found"}

    def test_submit_application_not_found():
        response = client.post(
            "/submit-application",
            json={"application_id": 999},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Application not found"}

    def test_ask_question_unrecognized():
        response = client.post(
            "/ask-question",
            data={"question": "unrecognized question"},
        )
        assert response.status_code == 200
        assert response.json() == {"answer": "This is a standard answer"}

    def test_add_to_wishlist_user_not_found():
        response = client.post(
            "/add-to-wishlist",
            json={"user_id": 999, "office_id": 1},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_manage_applications_admin_not_found():
        response = client.post(
            "/manage-applications",
            json={"admin_id": 999},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Admin not found"}

    def test_manage_offices_admin_not_found():
        response = client.post(
            "/manage-offices",
            json={"admin_id": 999},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Admin not found"}

    def test_manage_users_admin_not_found():
        response = client.post(
            "/manage-users",
            json={"admin_id": 999},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Admin not found"}

    def test_generate_report_admin_not_found():
        response = client.post(
            "/generate-report",
            json={"admin_id": 999},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Admin not found"}

    def test_export_report_admin_not_found():
        response = client.post(
            "/export-report",
            json={"admin_id": 999},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Admin not found"}
