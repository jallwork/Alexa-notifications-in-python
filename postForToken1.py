import time
import datetime
import json
import requests
import credentials

# constants
UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
TOKEN_URI = "https://api.amazon.com/auth/o2/token"


# Token access constants
CLIENT_ID = credentials.key['CLIENT_ID']
CLIENT_SECRET = credentials.key['CLIENT_SECRET']

def get_access_token():

    token_params = {
        "grant_type" : "client_credentials",
        "scope": "alexa::proactive_events",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    token_headers = {
        "Content-Type": "application/json;charset=UTF-8"
    }

    response = requests.post(TOKEN_URI, headers=token_headers, data=json.dumps(token_params), allow_redirects=True)

    print("Token response header: " + format(response.headers))
    print("Token response status: " + format(response.status_code))
    print("Token response body  : " + format(response.text))

    if response.status_code != 200:
        print("Error obtaining access code!")
        return None

    access_token = json.loads(response.text)["access_token"]
    return access_token

def main():

    """Main function that requests Auth token from AMAZON """ 

    token = get_access_token()
    print (token)

if __name__ == "__main__":
    main()