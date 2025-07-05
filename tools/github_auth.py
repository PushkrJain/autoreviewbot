# tools/github_auth.py

import time
import jwt
import yaml
import httpx


def get_jwt() -> str:
    """
    Generate a JWT for GitHub App authentication.
    Returns:
        A signed JWT as a string.
    """
    # Load GitHub App credentials from config file
    with open("config/github_app.yaml") as f:
        cfg = yaml.safe_load(f)

    app_id = cfg["app_id"]
    private_key_path = cfg["private_key_path"]

    # Read the private key
    with open(private_key_path, "r") as f:
        private_key = f.read()

    # Define issued-at and expiry timestamps
    now = time.time()
    iat = int(now)
    exp = iat + 600  # Token valid for 10 minutes

    payload = {
        "iat": iat,
        "exp": exp,
        "iss": app_id,
    }

    # Sign the JWT using RS256
    encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256")

    # Ensure the token is a string (PyJWT ≥ 2.0 returns bytes)
    if isinstance(encoded_jwt, bytes):
        encoded_jwt = encoded_jwt.decode("utf-8")

    return encoded_jwt


def get_installation_token() -> str | None:
    """
    Retrieve a GitHub App installation token using the JWT.
    Returns:
        Installation token string if successful, else None.
    """
    jwt_token = get_jwt()
    installation_id = 74443799  # Replace with your correct installation ID

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }

    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"

    response = httpx.post(url, headers=headers)

    if response.status_code == 201:
        return response.json()["token"]
    else:
        print(f"❌ Installation token request failed: {response.status_code}")
        print(response.text)
        return None

