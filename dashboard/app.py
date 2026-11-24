
import os
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from authlib.integrations.flask_client import OAuth


# Load environment variables from the project root
load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY is missing from the .env file.")

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


# AWS API configuration
BASE_API_URL = "https://3rqqcfw2va.execute-api.ap-southeast-2.amazonaws.com"

READINGS_API_URL = f"{BASE_API_URL}/readings"
INCIDENTS_API_URL = f"{BASE_API_URL}/incidents"
HISTORY_API_URL = f"{BASE_API_URL}/incidents/history"
UPDATE_INCIDENT_API_URL = f"{BASE_API_URL}/incidents/update"


# Cognito configuration
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN", "").rstrip("/")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
COGNITO_ISSUER = os.getenv("COGNITO_ISSUER", "").rstrip("/")

if not all([
    COGNITO_DOMAIN,
    COGNITO_CLIENT_ID,
    COGNITO_CLIENT_SECRET,
    COGNITO_ISSUER
]):
    raise RuntimeError("One or more Cognito settings are missing from .env.")


# Configure Cognito OAuth login
oauth = OAuth(app)

oauth.register(
    name="cognito",
    client_id=COGNITO_CLIENT_ID,
    client_secret=COGNITO_CLIENT_SECRET,
    server_metadata_url=(
        f"{COGNITO_ISSUER}/.well-known/openid-configuration"
    ),
    client_kwargs={
        "scope": "openid email"
    }
)


# Retrieve environmental readings
def get_readings():
    try:
        response = requests.get(
            READINGS_API_URL,
            params={"device_id": "server_room_001", "limit": 50},
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        print(f"Unable to retrieve readings: {error}")
        return []


# Retrieve active incidents
def get_incidents():
    try:
        response = requests.get(INCIDENTS_API_URL, timeout=10)
        response.raise_for_status()

        incidents = response.json()
        return incidents if isinstance(incidents, list) else []

    except requests.exceptions.RequestException as error:
        print(f"Unable to retrieve incidents: {error}")
        return []


# Retrieve incident history
def get_incident_history():
    try:
        response = requests.get(HISTORY_API_URL, timeout=10)
        response.raise_for_status()

        history = response.json()
        return history if isinstance(history, list) else []

    except requests.exceptions.RequestException as error:
        print(f"Unable to retrieve incident history: {error}")
        return []


# Home page
@app.route("/")
def home():
    if session.get("role") == "Administrator":
        return redirect(url_for("admin_dashboard"))

    if session.get("role") == "Technician":
        return redirect(url_for("technician_dashboard"))

    return redirect(url_for("login"))


# Cognito login
@app.route("/login")
def login():
    session.clear()

    callback_url = url_for("callback", _external=True)

    return oauth.cognito.authorize_redirect(callback_url)


# Cognito callback
@app.route("/callback")
def callback():
    try:
        token = oauth.cognito.authorize_access_token()

        # Read the verified OpenID Connect user claims
        user_info = token.get("userinfo")

        if not user_info:
            user_info = oauth.cognito.parse_id_token(token)

        groups = user_info.get("cognito:groups", [])

        # Administrator takes priority if a user belongs to both groups
        if "Administrator" in groups:
            role = "Administrator"

        elif "Technician" in groups:
            role = "Technician"

        else:
            session.clear()
            return (
                "Access denied. Your Cognito account is not assigned "
                "to an authorised group.",
                403
            )

        session["role"] = role
        session["user_email"] = user_info.get("email", "")
        session["user_id"] = user_info.get("sub", "")

        return redirect(url_for("home"))

    except Exception as error:
        print(f"Cognito login failed: {error}")
        session.clear()
        return "Login failed. Please try again.", 401


# Administrator dashboard
@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "Administrator":
        return redirect(url_for("login"))

    readings = get_readings()
    incidents = get_incidents()
    incident_history = get_incident_history()

    total_readings = len(readings)
    latest_reading = readings[0] if readings else None

    normal_count = sum(
        1 for reading in readings
        if reading.get("status") == "NORMAL"
    )

    warning_count = sum(
        1 for reading in readings
        if reading.get("status") == "WARNING"
    )

    critical_count = sum(
        1 for reading in readings
        if reading.get("status") == "CRITICAL"
    )

    return render_template(
        "admin.html",
        readings=readings,
        incidents=incidents,
        incident_history=incident_history,
        total_readings=total_readings,
        latest_reading=latest_reading,
        normal_count=normal_count,
        warning_count=warning_count,
        critical_count=critical_count,
        active_incident_count=len(incidents)
    )


# Technician dashboard
@app.route("/technician")
def technician_dashboard():
    if session.get("role") != "Technician":
        return redirect(url_for("login"))

    incidents = get_incidents()

    return render_template(
        "technician.html",
        incidents=incidents
    )


# Technician incident actions
@app.route("/technician/action", methods=["POST"])
def technician_action():
    if session.get("role") != "Technician":
        return redirect(url_for("login"))

    action = request.form.get("action")
    device_id = request.form.get("device_id")

    if not device_id:
        flash("Device ID is missing.", "error")
        return redirect(url_for("technician_dashboard"))

    data = {
        "action": action,
        "device_id": device_id
    }

    if action == "SUBMIT_REPORT":
        data["report"] = request.form.get("report", "").strip()

        if not data["report"]:
            flash("Please enter a maintenance report.", "error")
            return redirect(url_for("technician_dashboard"))

    elif action == "RESOLVE":
        data["resolution_note"] = request.form.get(
            "resolution_note", ""
        ).strip()

        if not data["resolution_note"]:
            flash("Please enter a resolution note.", "error")
            return redirect(url_for("technician_dashboard"))

    elif action != "ACKNOWLEDGE":
        flash("Invalid technician action.", "error")
        return redirect(url_for("technician_dashboard"))

    try:
        response = requests.post(
            UPDATE_INCIDENT_API_URL,
            json=data,
            timeout=15
        )

        response.raise_for_status()
        result = response.json()

        flash(
            result.get("message", "Action completed successfully."),
            "success"
        )

    except requests.exceptions.RequestException as error:
        print(f"Unable to update incident: {error}")
        flash(
            "Unable to update the incident. Please try again.",
            "error"
        )

    except ValueError:
        flash("The server returned an invalid response.", "error")

    return redirect(url_for("technician_dashboard"))


# Cognito logout
@app.route("/logout")
def logout():
    session.clear()

    app_url = os.getenv(
        "APP_BASE_URL",
        "http://localhost:5000"
    ).rstrip("/")

    logout_url = (
        f"{COGNITO_DOMAIN}/logout?"
        + urlencode({
            "client_id": COGNITO_CLIENT_ID,
            "logout_uri": f"{app_url}/login"
        })
    )

    return redirect(logout_url)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
