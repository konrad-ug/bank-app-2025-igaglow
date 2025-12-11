import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api/accounts"

@pytest.fixture
def create_test_account():
    payload = {
        "name": "James",
        "surname": "Hetfield",
        "pesel": "12345678901"
    }
    requests.post(BASE_URL, json=payload)
    return payload["pesel"]


@pytest.fixture
def delete_test_account(create_test_account):
    yield
    requests.delete(f"{BASE_URL}/{create_test_account}")

def test_create_account():
    payload = {
        "name": "James",
        "surname": "Hetfield",
        "pesel": "12345678901"
    }

    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["message"] == "Account created"

def test_get_account_by_pesel(create_test_account):
    pesel = create_test_account
    print(pesel)
    response = requests.get(f"{BASE_URL}/{pesel}")

    assert response.status_code == 200
    data = response.json()

    assert data["pesel"] == pesel
    assert data["name"] == "James"
    assert data["surname"] == "Hetfield"
    assert "balance" in data


def test_get_account_not_found():
    response = requests.get(f"{BASE_URL}/00000000000")
    assert response.status_code == 404

def test_update_account(create_test_account):
    pesel = create_test_account

    update_payload = {"name": "James"}

    response = requests.patch(f"{BASE_URL}/{pesel}", json=update_payload)
    assert response.status_code == 200

    get_response = requests.get(f"{BASE_URL}/{pesel}")
    data = get_response.json()


    assert data["name"] == "James"
    assert data["surname"] == "Hetfield"

def test_delete_account(create_test_account):
    pesel = create_test_account

    response = requests.delete(f"{BASE_URL}/{pesel}")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Account deleted"




