import time

import requests

from .shared import token_url


class AuthorizationGrant:
    def __init__(self, client_id, client_secret, username, password):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None
        self.access_token_expires_at = 0
        self.refresh_token_expires_at = 0

    def get_token(self, grant_type="password", refresh_token=None):
        payload = {"grant_type": grant_type, "client_id": self.client_id, "client_secret": self.client_secret, "platform": "pc"}

        if grant_type == "password":
            payload.update(
                {
                    "username": self.username,
                    "password": self.password,
                }
            )
        elif grant_type == "refresh_token":
            payload.update({"refresh_token": refresh_token})

        response = requests.post(self.token_url, data=payload, timeout=5)

        if response.status_code == 200:
            token_info = response.json()
            self.access_token = token_info["access_token"]
            self.refresh_token = token_info["refresh_token"]
            self.access_token_expires_at = time.time() + token_info["expires_in"]
            self.refresh_token_expires_at = time.time() + token_info["refresh_token_expires_in"]

    def is_access_token_expired(self):
        return time.time() >= self.access_token_expires_at

    def is_refresh_token_expired(self):
        return time.time() >= self.refresh_token_expires_at

    def ensure_access_token(self):
        if not self.access_token or self.is_access_token_expired():
            if self.refresh_token and not self.is_refresh_token_expired():
                self.get_token(grant_type="refresh_token", refresh_token=self.refresh_token)
            else:
                self.get_token()

    def make_request(self, method, url, **kwargs):
        self.ensure_access_token()

        headers = kwargs.get("headers", {})
        headers.update({"Authorization": f"Bearer {self.access_token}"})
        kwargs["headers"] = headers

        response = requests.request(method, url, **kwargs)
        return response
