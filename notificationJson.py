import time
import uuid
import datetime
import json
import requests
import credentials

# Token access constants
CLIENT_ID = credentials.key['CLIENT_ID']
CLIENT_SECRET = credentials.key['CLIENT_SECRET']
UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
TOKEN_URI = "https://api.amazon.com/auth/o2/token"
ALEXA_URI = "https://api.eu.amazonalexa.com/v1/proactiveEvents/stages/development"


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

    print("Token response status: " + format(response.status_code))
    print("Token response body  : " + format(response.text))

    if response.status_code != 200:
        print("Error calling LWA!")
        return None

    access_token = json.loads(response.text)["access_token"]
    return access_token

token = get_access_token()

headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json;charset=UTF-8"
    }

seconds = time.time()
timestamp  = time.strftime(UTC_FORMAT, time.gmtime(seconds))
reference_id = str(uuid.uuid4())
seconds +=3600	# 1 hour for demo
expiry_time =  time.strftime(UTC_FORMAT, time.gmtime(seconds))

params = {
    "timestamp": timestamp,
    "referenceId": reference_id,
    "expiryTime": expiry_time,

    "event": {
        "name": "AMAZON.MessageAlert.Activated",
        "payload": {
            "state": {
                "status": "UNREAD",
                "freshness": "NEW"
            },
            "messageGroup": {
                "creator": {
                    "name": "Johns python program"
                },
                "count": 1
            }
        }
    },
    "localizedAttributes": [
      {
        "locale": "en-GB",
        "providerName": "Alexa Events Example",
        "contentName": "Some content"
      }
    ],
    "relevantAudience": {
        "type": "Multicast",
        "payload": { }
    }
}

response = requests.post(ALEXA_URI, headers=headers, data=json.dumps(params), allow_redirects=True)
print("done" , response)
