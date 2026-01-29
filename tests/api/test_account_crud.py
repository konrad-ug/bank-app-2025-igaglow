import pytest
import requests
import random

pytestmark = pytest.mark.api

BASE_URL = "http://127.0.0.1:5000/api/accounts"
TRANSFER_URL = f"{BASE_URL}/{{}}/transfer"

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
    assert response.status_code in (201, 409)
    data = response.json()

    assert data["message"] in ("Account created", "Account with this pesel already exists")


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

def random_pesel():
    return "".join(str(random.randint(0, 9)) for _ in range(11))

def test_create_account_duplicate_pesel():
    pesel = random_pesel()

    payload = {
        "name": "James",
        "surname": "Hetfield",
        "pesel": pesel
    }

    r1 = requests.post(BASE_URL, json=payload)
    r2 = requests.post(BASE_URL, json=payload)

    assert r1.status_code == 201
    assert r2.status_code == 409


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


def test_transfer_account_not_found():
    r = requests.post(
        TRANSFER_URL.format("00000000000"),
        json={"amount": 100, "type": "incoming"}
    )
    assert r.status_code == 404


def test_transfer_incoming(create_test_account):
    pesel = create_test_account

    r = requests.post(
        TRANSFER_URL.format(pesel),
        json={"amount": 500, "type": "incoming"}
    )
    assert r.status_code == 200

def test_transfer_outgoing_success(create_test_account):
    pesel = create_test_account

    requests.post(
        TRANSFER_URL.format(pesel),
        json={"amount": 500, "type": "incoming"}
    )

    r = requests.post(
        TRANSFER_URL.format(pesel),
        json={"amount": 200, "type": "outgoing"}
    )
    assert r.status_code == 200

def test_transfer_outgoing_not_enough_money(create_test_account):
    pesel = create_test_account

    r = requests.post(
        TRANSFER_URL.format(pesel),
        json={"amount": 1000, "type": "outgoing"}
    )
    assert r.status_code == 422

def test_transfer_unknown_type(create_test_account):
    pesel = create_test_account

    r = requests.post(
        TRANSFER_URL.format(pesel),
        json={"amount": 100, "type": "magic"}
    )
    assert r.status_code == 400


# @pytest.fixture
# def delete_test_account(create_test_account):
#     yield
#     requests.delete(f"{BASE_URL}/{create_test_account}")
#
#
# def test_create_account(test_account_payload, delete_test_account):
#     response = requests.post(BASE_URL, json=test_account_payload)
#
#     assert response.status_code == 201
#     data = response.json()
#
#     assert data["message"] == "Account created"
#
#
# def test_create_account_duplicate_pesel(create_test_account):
#     response = requests.post(BASE_URL, json=create_test_account)
#
#     assert response.status_code == 409
#     data = response.json()
#     assert data["message"] == "Account with this pesel already exists"





