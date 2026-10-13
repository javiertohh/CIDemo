from flask import Flask, jsonify, request

from duckfine import DuckFine

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/fine")
def fine():
    days_value = request.args.get("days")

    try:
        days = int(days_value) if days_value is not None else None
    except ValueError:
        days = None

    if days is None or days < 0:
        return jsonify({"error": "days must be a non-negative integer"}), 400

    deluxe = request.args.get("deluxe") == "1"
    fee = DuckFine("api").charge(days, deluxe=deluxe)
    return jsonify({"fee": fee})
