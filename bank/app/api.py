from flask import Flask, request, jsonify

from bank.src.account_registry import AccountsRegistry
from bank.src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountsRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    if not data or not all(k in data for k in ("name", "surname", "pesel")):
        return jsonify({"error": "Invalid request body"}), 400

    if registry.find_by_pesel(data["pesel"]):
        return jsonify({"message": "Account with this pesel already exists"}), 409

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
    return jsonify({"count": registry.count_accounts()}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    selected_account = registry.find_by_pesel(pesel)
    if not selected_account:
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
    acc = registry.find_by_pesel(pesel)

    if not acc:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json()

    if "name" in data:
        acc.first_name = data["name"]

    if "surname" in data:
        acc.last_name = data["surname"]

    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    acc = registry.find_by_pesel(pesel)
    if not acc:
        return jsonify({"error": "Account not found"}), 404

    registry.accounts.remove(acc)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=["POST"])
def transfer(pesel):
    acc = registry.find_by_pesel(pesel)
    if not acc:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json() or {}
    if "amount" not in data or "type" not in data:
        return jsonify({"error": "Invalid request body"}), 400

    amount = data["amount"]
    transfer_type = data["type"]

    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    if transfer_type not in ("incoming", "outgoing", "express"):
        return jsonify({"error": "Unknown transfer type"}), 400

    # ---------- INCOMING ----------
    if transfer_type == "incoming":
        acc.balance += amount
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200

    # ---------- OUTGOING ----------
    if transfer_type == "outgoing":
        if acc.balance < amount:
            return jsonify({"error": "Not enough funds"}), 422
        acc.balance -= amount
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200

    # ---------- EXPRESS ----------
    if transfer_type == "express":
        total = amount + 1.0
        if acc.balance < total:
            return jsonify({"error": "Not enough funds"}), 422
        acc.balance -= total
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
