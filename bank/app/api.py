from flask import Flask, request, jsonify

from bank.src.account_registry import AccountsRegistry
from bank.src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountsRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")

    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.get_all_accounts()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel":
    acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.count_accounts()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    selected_account = registry.find_by_pesel(pesel)
    if selected_account is None:
        return jsonify({"error": "Account not found"}), 404

    data = {
        "name": selected_account.first_name,
        "surname": selected_account.last_name,
        "pesel": selected_account.pesel,
        "balance": selected_account.balance
    }

    return jsonify(data), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    acc = registry.find_by_pesel(pesel)

    if acc is None:
        return jsonify({"error": "Account not found"}), 404

    if "name" in data:
        acc.first_name = data["name"]

    if "surname" in data:
        acc.last_name = data["surname"]

    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    acc = registry.find_by_pesel(pesel)
    registry.accounts.remove(acc)
    return jsonify({"message": "Account deleted"}), 200