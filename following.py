import requests
import os
import json

def auth():
    return os.environ.get("BEARER_TOKEN")


def create_url():
    user_id = 928331587636420608
    return "https://api.twitter.com/2/users/{}/following".format(user_id)


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def main():
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers, params=None)
    return get_followers(json_response)

def get_followers(json_response):
    following = []
    for user in json_response["data"]:
        following.append(user["username"])
    return following
