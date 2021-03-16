from pathlib import Path
from requests_oauthlib import OAuth2Session
import json
import os

## const variables
api_url = "https://photoslibrary.googleapis.com/v1/mediaItems"
scope = ["https://www.googleapis.com/auth/photoslibrary.readonly"]
# credential_file_path="F:\Documents\git\GooglePhotoAlbumOrganizer\credential\credentials.json"
credential_file_path = (
    os.path.dirname(os.path.basename(__file__)) + "..\credential\credentials.json"
)


def save_token(token):
    token = {
        "access_token": token.get("access_token"),
        "refresh_token": token.get("refresh_token"),
        "token_type": token.get("token_type"),
        "expires_in": token.get("expires_in"),
    }
    Path("token.json").write_text(json.dumps(token))


def load_token():
    # if not exist, return expired dummy
    token = {
        "access_token": "",
        "refresh_token": "",
        "token_type": "",
        "expires_in": "-30",
    }
    path = Path("token.json")
    if path.exists():
        token = json.loads(path.read_text())
    return token


# return session object with login
def login():
    # load credential
    app_type = "web"
    auth_info = json.loads(Path(credential_file_path).read_text()).get(app_type, None)
    assert auth_info is not None

    token = load_token()
    # credential for refresh token
    extras = {
        "client_id": auth_info.get("client_id"),
        "client_secret": auth_info.get("client_secret"),
    }
    # generate session object
    google = OAuth2Session(
        auth_info.get("client_id"),
        scope=scope,
        token=token,
        auto_refresh_kwargs=extras,
        token_updater=save_token,
        auto_refresh_url=auth_info.get("token_uri"),
        redirect_uri=auth_info.get("redirect_uris")[0],
    )
    # login if not login
    if not google.authorized:
        authorization_url, state = google.authorization_url(
            auth_info.get("auth_uri"), access_type="offline", prompt="select_account"
        )
        # paste code with accress url
        print("Access {} and paste code.".format(authorization_url))
        access_code = input(">>> ")
        google.fetch_token(
            auth_info.get("token_uri"),
            client_secret=auth_info.get("client_secret"),
            code=access_code,
        )
        assert google.authorized
        # dave token TODO
        save_token(google.token)
    return google


def test():
    google = login()
    # get Photos contents
    response = google.get(api_url)
    print(response.text)