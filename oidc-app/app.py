import os
import requests
from flask import Flask, redirect, request, render_template, session

app = Flask(__name__)
app.secret_key = "secret"

CLIENT_ID = os.getenv("OIDC_CLIENT_ID")
CLIENT_SECRET = os.getenv("OIDC_CLIENT_SECRET")

KEYCLOAK = "http://keycloak:8080"
REALM = "demo"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return redirect(
        f"http://localhost:8080/realms/{REALM}/protocol/openid-connect/auth"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri=http://localhost:5000/callback"
        f"&scope=openid profile email"
    )

@app.route('/callback')
def callback():
    code = request.args.get('code')

    token = requests.post(
        f"{KEYCLOAK}/realms/{REALM}/protocol/openid-connect/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": "http://localhost:5000/callback"
        }
    ).json()

    user = requests.get(
        f"{KEYCLOAK}/realms/{REALM}/protocol/openid-connect/userinfo",
        headers={"Authorization": f"Bearer {token['access_token']}"}
    ).json()

    session['user'] = user

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect('/')
    return render_template("dashboard.html", user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
