import streamlit as st
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")
CALLBACK_URL = os.getenv("TWITTER_CALLBACK_URL")
AUTHORIZATION_BASE_URL = "https://twitter.com/i/oauth2/authorize"
# AUTHORIZATION_BASE_URL="https://x.com/i/flow/login"
TOKEN_URL = "https://api.twitter.com/oauth/request_token"

# OAuth scopes
SCOPES = [
    "tweet.read",
    "users.read",
    "follows.read",
    "offline.access"
]

st.title("Twitter Login with Streamlit")

if "oauth_token" not in st.session_state:
    st.session_state["oauth_token"] = None

if st.session_state["oauth_token"]:
    # Logged in successfully
    st.success("You are logged in to Twitter!")
    st.write("Access Token:", st.session_state["oauth_token"])
else:
    # Initialize OAuth2 session
    twitter = OAuth2Session(
        CLIENT_ID,
        redirect_uri=CALLBACK_URL,
        scope=SCOPES
    )

    # Step 1: Get the authorization URL
    authorization_url, state = twitter.authorization_url(AUTHORIZATION_BASE_URL)
    st.write("Click below to log in to Twitter:")
    st.markdown(f"[Login to Twitter]({authorization_url})")

    # Step 2: Handle the callback
    callback_code = st.text_input("Paste the callback URL after login:")
    if callback_code:
        # Extract the code from the callback URL
        from urllib.parse import urlparse, parse_qs

        query_params = parse_qs(urlparse(callback_code).query)
        authorization_response = query_params.get("code", [None])[0]

        if authorization_response:
            # Step 3: Fetch the access token
            token = twitter.fetch_token(
                TOKEN_URL,
                client_secret=CLIENT_SECRET,
                code=authorization_response
            )
            st.session_state["oauth_token"] = token
            st.success("Successfully authenticated with Twitter!")

   # Optionally, you can add a logout button
    if st.button("Logout"):
     st.session_state.clear()  # Clear session state
     st.success("Logged out successfully.")
