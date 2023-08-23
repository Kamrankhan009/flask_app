from flask import Flask, request, redirect, session
import requests
from oauthlib.oauth2 import WebApplicationClient

app = Flask(__name__)

# Replace these values with your own
DISCORD_CLIENT_ID = "1143875517909565480"
DISCORD_CLIENT_SECRET = "a-eUXc4rnvc_ie1J97jMOyiQ_7c4sj1i"
DISCORD_REDIRECT_URI = "http://localhost:5000/callback"
DISCORD_API_BASE_URL = "https://discord.com/api"
DISCORD_OAUTH_AUTHORIZE_URL = "https://discord.com/api/oauth2/authorize"
DISCORD_OAUTH_TOKEN_URL = "https://discord.com/api/oauth2/token"

client = WebApplicationClient(DISCORD_CLIENT_ID)

@app.route("/")
def index():
    return "Welcome to the login page!"

@app.route("/login")
def login():
    redirect_uri = client.prepare_request_uri(DISCORD_OAUTH_AUTHORIZE_URL, redirect_uri=DISCORD_REDIRECT_URI, scope=["identify"])
    return redirect(redirect_uri)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_url, headers, body = client.prepare_token_request(DISCORD_OAUTH_TOKEN_URL, code=code, redirect_url=DISCORD_REDIRECT_URI)
    token_response = requests.post(token_url, headers=headers, data=body, auth=(DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET))

    client.parse_request_body_response(token_response.content.decode("utf-8"))

    userinfo_url = f"{DISCORD_API_BASE_URL}/users/@me"
    userinfo_response = requests.get(userinfo_url, headers={"Authorization": f"Bearer {client.token['access_token']}"})
    user_info = userinfo_response.json()
    avatar_hash = user_info["avatar"]

    user_id = user_info['id']
    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png"

    return f"Logged in as: {user_info['username']}#{user_info['discriminator']} <br><img src='{avatar_url}' alt='Avatar'>"

if __name__ == "__main__":
    app.run(debug=True)
