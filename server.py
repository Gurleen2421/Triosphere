from flask import Flask, request, jsonify

app = Flask(__name__)

# Store current active request
active_request = None
accepted_by = None

@app.route("/send_request", methods=["POST"])
def send_request():
    global active_request, accepted_by
    data = request.json
    active_request = data["message"]
    accepted_by = None
    print(f"📩 New Request: {active_request}")
    return jsonify({"status": "Request received", "request": active_request})

@app.route("/get_request", methods=["GET"])
def get_request():
    if active_request and not accepted_by:
        return jsonify({"request": active_request})
    return jsonify({"request": None})

@app.route("/accept_request", methods=["POST"])
def accept_request():
    global accepted_by, active_request
    data = request.json
    if not accepted_by:  # First one to accept wins
        accepted_by = data["laptop"]
        print(f"✅ Accepted by {accepted_by}")
        return jsonify({"status": "accepted", "by": accepted_by})
    else:
        return jsonify({"status": "already accepted", "by": accepted_by})

@app.route("/ack_phone", methods=["GET"])
def ack_phone():
    if accepted_by:
        return jsonify({"status": "accepted", "by": accepted_by})
    return jsonify({"status": "pending"})


if __name__ == "__main__":
    # Run on laptop’s hotspot IP
    app.run(host="0.0.0.0", port=5000)