# Instagram DM to Telegram Post Link Integration Guide

This document outlines the steps required to create a bot that automatically responds to Instagram Direct Messages (DMs) with a link to a specific Telegram channel post.

## Goal

When a user sends a Direct Message to a specific Instagram account, a bot should automatically reply with a predefined message containing an anchor link to a specific post within a Telegram channel.

## Prerequisites

1.  **Facebook Developer Account:** You need an account at [https://developers.facebook.com/](https://developers.facebook.com/).
2.  **Facebook App:** Create a new Facebook App within the Developer Dashboard.
3.  **Instagram Business or Creator Account:** The Instagram account that will receive the DMs must be a Business or Creator account.
4.  **Facebook Page:** A Facebook Page linked to the Instagram Business/Creator account.
5.  **Permissions:** Your Facebook App needs the `instagram_manage_messages` permission granted through the App Review process (though you can test with developers/admins before full review).
6.  **Publicly Accessible HTTPS URL:** You need a server or service (like Cloud Run, Heroku, AWS Lambda, etc.) with a stable HTTPS URL to receive webhook notifications from Instagram/Facebook.
7.  **Telegram Post Link:** The full URL to the specific Telegram post (e.g., `https://t.me/YourChannelUsername/12345`).

## Technical Steps

1.  **Configure Facebook App & Instagram:**
    *   In the Facebook Developer Dashboard for your App, add the "Messenger" product.
    *   In the Messenger settings, configure "Instagram Messaging".
    *   Link your Facebook Page (which is linked to your Instagram account).
    *   Generate a Page Access Token. **Store this securely!** (e.g., in an environment variable `INSTAGRAM_PAGE_ACCESS_TOKEN`).

2.  **Set Up Webhooks:**
    *   In the Messenger -> Instagram Messaging settings, configure Webhooks.
    *   Provide your publicly accessible HTTPS endpoint URL (e.g., `https://your-service-url.com/webhook`).
    *   Create a **Verify Token**. This is a secret string you define. **Store this securely!** (e.g., `INSTAGRAM_WEBHOOK_VERIFY_TOKEN`). Facebook will use this to verify your endpoint.
    *   Subscribe to the `messages` webhook field for your linked Facebook Page.

3.  **Create a Web Server Backend:**
    *   Choose a web framework (e.g., Flask, FastAPI, Express).
    *   Create two endpoints:
        *   `GET /webhook`: Handles the webhook verification request from Facebook. It must check if the `hub.verify_token` query parameter matches your `INSTAGRAM_WEBHOOK_VERIFY_TOKEN` and respond with the `hub.challenge` value.
        *   `POST /webhook`: Receives the actual message notifications from Instagram.

4.  **Handle Incoming Messages (`POST /webhook`):**
    *   **Verify Signature (Security):** Verify the `X-Hub-Signature-256` header using your App Secret to ensure the request genuinely came from Facebook.
    *   **Parse Payload:** The request body will contain JSON data about the incoming message(s). Extract the sender's ID (`sender.id`) and the message content (if needed, though for this simple case, just replying might be enough).
    *   **Avoid Loops:** Ensure the bot doesn't reply to its own messages. Check if the sender ID is the same as your Page/Bot ID.
    *   **Construct Telegram Link:** Define the specific Telegram post link (e.g., `TELEGRAM_POST_URL = "https://t.me/YourChannelUsername/12345"`). Store this preferably in an environment variable.
    *   **Construct Reply Message:** Create the reply text, including the Telegram link.

5.  **Send Reply via Instagram Graph API:**
    *   Use the `sender.id` obtained from the webhook payload as the `recipient.id`.
    *   Make a `POST` request to the Facebook Graph API endpoint: `https://graph.facebook.com/v19.0/me/messages` (use the latest stable API version).
    *   Include your `INSTAGRAM_PAGE_ACCESS_TOKEN` in the request (e.g., as a query parameter `access_token=YOUR_TOKEN`).
    *   The request body should be JSON, specifying the recipient and the message text:
        ```json
        {
          "recipient": {
            "id": "<PSID_FROM_WEBHOOK>"
          },
          "message": {
            "text": "Here is the link you requested: https://t.me/YourChannelUsername/12345"
          }
        }
        ```

6.  **Deployment:**
    *   Deploy your web server application to a platform that provides a public HTTPS URL (Cloud Run, Heroku, etc.).
    *   Configure necessary environment variables (`INSTAGRAM_PAGE_ACCESS_TOKEN`, `INSTAGRAM_WEBHOOK_VERIFY_TOKEN`, `TELEGRAM_POST_URL`, potentially `FACEBOOK_APP_SECRET`).

## Example (Conceptual Python/Flask)

```python
import os
import hmac
import hashlib
import json
from flask import Flask, request, abort, Response

app = Flask(__name__)

# Load from environment variables
FB_APP_SECRET = os.environ.get("FACEBOOK_APP_SECRET")
VERIFY_TOKEN = os.environ.get("INSTAGRAM_WEBHOOK_VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.environ.get("INSTAGRAM_PAGE_ACCESS_TOKEN")
TELEGRAM_POST_URL = os.environ.get("TELEGRAM_POST_URL", "YOUR_TELEGRAM_POST_URL_HERE") # Provide a default or ensure it's set

@app.route('/webhook', methods=['GET'])
def webhook_verify():
    """ Handle webhook verification """
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN:
        print("Webhook verified!")
        return request.args.get('hub.challenge'), 200
    else:
        print("Webhook verification failed.")
        return 'Forbidden', 403

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """ Handle incoming messages """
    # Verify request signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        print("Missing signature.")
        abort(400)

    hash_object = hmac.new(FB_APP_SECRET.encode('utf-8'), msg=request.data, digestmod=hashlib.sha256)
    expected_signature = 'sha256=' + hash_object.hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        print("Invalid signature.")
        abort(400)

    # Process incoming message event
    data = request.get_json()
    print("Received webhook data:", json.dumps(data, indent=2)) # Log for debugging

    if data.get("object") == "instagram":
        for entry in data.get("entry", []):
            for message_event in entry.get("messaging", []):
                if message_event.get("message"): # Check if it's a message event
                    sender_id = message_event["sender"]["id"]
                    # Optional: Check if message is from user, not page itself
                    # recipient_id = message_event["recipient"]["id"]
                    # if sender_id == your_page_id: continue

                    print(f"Received message from sender ID: {sender_id}")
                    send_reply(sender_id, f"Here's the link: {TELEGRAM_POST_URL}")

    return "EVENT_RECEIVED", 200

def send_reply(recipient_id, message_text):
    """ Sends message back to user via Instagram Graph API """
    import requests # Use requests library

    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    })

    graph_api_url = "https://graph.facebook.com/v19.0/me/messages" # Use appropriate version
    try:
        response = requests.post(graph_api_url, params=params, headers=headers, data=data)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"Successfully sent reply to {recipient_id}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending reply to {recipient_id}: {e}")
        if e.response is not None:
            print(f"Response body: {e.response.text}")


if __name__ == '__main__':
    # Make sure to set environment variables before running
    if not all([FB_APP_SECRET, VERIFY_TOKEN, PAGE_ACCESS_TOKEN, TELEGRAM_POST_URL]):
         print("ERROR: Missing required environment variables (FACEBOOK_APP_SECRET, INSTAGRAM_WEBHOOK_VERIFY_TOKEN, INSTAGRAM_PAGE_ACCESS_TOKEN, TELEGRAM_POST_URL)")
    else:
        # Port should be configured based on deployment environment (e.g., PORT env var for Cloud Run)
        port = int(os.environ.get("PORT", 8080))
        app.run(host='0.0.0.0', port=port, debug=True) # Turn off debug in production

```

## Next Steps

1.  Follow the prerequisites to set up your Facebook App and Instagram connection.
2.  Obtain the necessary tokens and the specific Telegram post URL.
3.  Develop the web server application based on the steps above.
4.  Deploy the application and configure the webhook in the Facebook Developer Dashboard.
5.  Test thoroughly.
