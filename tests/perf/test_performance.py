import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api/accounts"


class TestApiPerformance:

    @pytest.fixture(autouse=True)
    def clean_registry(self):
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            accounts = response.json()
            for acc in accounts:
                requests.delete(f"{BASE_URL}/{acc['pesel']}")

    def test_create_and_delete_performance(self):
        for i in range(100):
            pesel = f"123456789{i:02d}"
            payload = {
                "name": "John",
                "surname": "Doe",
                "pesel": pesel
            }

            response_post = requests.post(BASE_URL, json=payload, timeout=0.5)
            assert response_post.status_code == 201
            assert response_post.elapsed.total_seconds() < 0.5

            response_delete = requests.delete(f"{BASE_URL}/{pesel}", timeout=0.5)
            assert response_delete.status_code == 200
            assert response_delete.elapsed.total_seconds() < 0.5

    def test_transfers_performance_and_balance(self):
        pesel = "99999999999"
        payload = {"name": "Rich", "surname": "Guy", "pesel": pesel}

        requests.post(BASE_URL, json=payload, timeout=0.5)

        for _ in range(100):
            transfer_data = {"amount": 10.0, "type": "incoming"}
            response = requests.post(f"{BASE_URL}/{pesel}/transfer", json=transfer_data, timeout=0.5)

            assert response.status_code == 200
            assert response.elapsed.total_seconds() < 0.5

        response_get = requests.get(f"{BASE_URL}/{pesel}", timeout=0.5)
        assert response_get.status_code == 200
        assert response_get.json()["balance"] == 1000.0

        requests.delete(f"{BASE_URL}/{pesel}")