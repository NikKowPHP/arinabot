# TODO List: Instagram DM to Telegram Post Link Integration

This checklist summarizes the tasks required to implement the Instagram DM bot based on the `instagram_telegram_integration_guide.md`.

## Phase 1: Setup & Configuration

-   [x] **Facebook Developer Account:** Ensure you have an active account.
-   [ ] **Create Facebook App:** Create a new App in the Facebook Developer Dashboard.
-   [ ] **Instagram Account:** Ensure the target Instagram account is a Business or Creator account.
-   [ ] **Link Facebook Page:** Link the Instagram account to a Facebook Page.
-   [ ] **Add Messenger Product:** Add the "Messenger" product to your Facebook App.
-   [ ] **Configure Instagram Messaging:** Set up Instagram Messaging within the Messenger product settings in your App.
-   [ ] **Link Page to App:** Link the correct Facebook Page within the Instagram Messaging settings.
-   [ ] **Generate Page Access Token:** Generate the token and store it securely (e.g., as `INSTAGRAM_PAGE_ACCESS_TOKEN` environment variable).
-   [ ] **Obtain Facebook App Secret:** Find your App Secret in the App's Basic Settings and store it securely (e.g., as `FACEBOOK_APP_SECRET` environment variable).
-   [ ] **Define Webhook Verify Token:** Create a secret string for webhook verification and store it securely (e.g., as `INSTAGRAM_WEBHOOK_VERIFY_TOKEN` environment variable).
-   [ ] **Get Telegram Post URL:** Determine the exact URL for the target Telegram post and store it (e.g., as `TELEGRAM_POST_URL` environment variable).
-   [ ] **Choose Deployment Platform:** Decide where the backend web server will be hosted (e.g., Cloud Run, Heroku, AWS Lambda) ensuring it provides a public HTTPS URL.

## Phase 2: Backend Development

-   [ ] **Choose Web Framework:** Select a Python web framework (e.g., Flask, FastAPI).
-   [ ] **Set up Project:** Create a new project directory, virtual environment, and install necessary libraries (e.g., `flask`, `requests`, `python-dotenv`).
-   [ ] **Implement `GET /webhook` Endpoint:** Create the route to handle Facebook's webhook verification requests, checking `hub.verify_token` and returning `hub.challenge`.
-   [ ] **Implement `POST /webhook` Endpoint:** Create the route to receive message notifications.
-   [ ] **Implement Signature Verification:** Add code to verify the `X-Hub-Signature-256` header using your `FACEBOOK_APP_SECRET`.
-   [ ] **Implement Payload Parsing:** Add code to parse the incoming JSON data, extracting the `sender.id`.
-   [ ] **Implement Anti-Loop Logic:** (Optional but recommended) Add a check to prevent the bot from replying to its own messages.
-   [ ] **Implement Reply Logic:** Construct the reply message using the `TELEGRAM_POST_URL`.
-   [ ] **Implement `send_reply` Function:** Create a function to make the `POST` request to the Facebook Graph API (`/me/messages`) using the `PAGE_ACCESS_TOKEN`, recipient ID, and message text.
-   [ ] **Add Error Handling:** Include try-except blocks for API calls and webhook processing.
-   [ ] **Add Logging:** Implement logging to track requests, responses, and errors.
-   [ ] **Load Environment Variables:** Ensure the application correctly loads all necessary secrets/config from environment variables.
-   [ ] **Create `requirements.txt`:** List all Python dependencies.
-   [ ] **Create `Dockerfile` (if using containers):** Define the container image.

## Phase 3: Deployment & Testing

-   [ ] **Deploy Application:** Deploy the backend server to your chosen platform.
-   [ ] **Get Public HTTPS URL:** Obtain the public URL for your deployed application's webhook endpoint.
-   [ ] **Configure Webhook URL in Facebook App:** Enter the public HTTPS URL (e.g., `https://your-app-url.com/webhook`) in the Messenger -> Instagram Messaging -> Webhooks settings.
-   [ ] **Subscribe to `messages` Field:** Ensure the webhook is subscribed to the `messages` field.
-   [ ] **Test Webhook Verification:** Facebook should send a `GET` request upon saving the webhook configuration. Check your server logs to confirm verification success.
-   [ ] **Request Permissions (if needed):** If testing beyond admins/developers, submit your App for `instagram_manage_messages` permission review.
-   [ ] **Test DM Functionality:** Send a DM to the linked Instagram account and check if the bot replies correctly with the Telegram link. Check server logs for details.
-   [ ] **Monitor:** Keep an eye on logs for any errors during operation.
