import http.client
import json
from dotenv import load_dotenv
import os
load_dotenv
# Replace with your Bot Token
tokens = os.getenv("SLACK_OUTH")
# Replace with the channel ID or name
CHANNEL_ID = "C080U7SH1B5"

def send_slack_notification(message):
    conn = http.client.HTTPSConnection("slack.com")
    headers = {
        "Authorization": f"Bearer {tokens}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": CHANNEL_ID,
        "text": message
    }

    # Convert payload to JSON
    payload_json = json.dumps(payload)

    try:
        # Make POST request
        conn.request("POST", "/api/chat.postMessage", body=payload_json, headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        response_json = json.loads(data)

        # Check if Slack returned an error
        if not response_json.get("ok"):
            print(f"Error sending message: {response_json.get('error')}")
    except Exception as e:
        print(f"HTTP Request failed: {e}")
    finally:
        conn.close()
