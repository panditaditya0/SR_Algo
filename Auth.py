from fyers_apiv3 import fyersModel
import os
import requests

client_id = app_id = "8IG3OQ82K3-100"
secret_key = app_secret = "SN0J43HZD8"
redirect_uri = redirect_url = "http://127.0.0.1:5500/index.html"
response_type = "code"
grant_type = "authorization_code"


def get_access_token(client_id, secret_key, self):
        session = fyersModel.SessionModel(
            client_id=client_id,
            secret_key=secret_key,
            redirect_uri=redirect_uri,
            response_type=response_type,
            grant_type=grant_type
        )
        response = session.generate_authcode()
        print("Login URL = ", response)
        return response, session


def get_access_token2(auth_code,session):
    if not os.path.exists("accessToken2.txt"):
        session.set_token(auth_code)
        resp = session.generate_token()
        access_token = resp["access_token"]
        with open("accessToken2.txt", "w") as f:
            f.write(access_token)
    else:
        print("Access token already exist")
        with open("accessToken2.txt", "r") as f:
            access_token = f.read()
    return access_token

def get_cached_access_token():
    with open("/Users/administrator/PycharmProjects/SR_Algo/UI/accessToken2.txt", "r") as f:
        access_token = f.read()
    return access_token