# Telegram Guide Bot - Implementation Plan

This document outlines the steps required to develop, test, and deploy the Telegram guide bot.
 pip3: Always prefer using python3 and pip3 to avoid conflicts with the older system Python 2 (if present).


**Project Files:**
*   `telegram_subscriber_bot_description.md`: Bot specifications and messages.
*   `telegram_bot/`: Directory containing bot code and resources.
*   `telegram_bot/guide.pdf`: Placeholder for the actual guide file.
*   `telegram_bot/bot.py`: Main bot script (to be completed).
*   `telegram_bot/requirements.txt`: Python dependencies (to be created).

---

## Phase 1: Setup & Initial Configuration

*   [ ] **Finalize Project Structure:**
    *   [X] Create `telegram_bot/` directory.
    *   [X] Create placeholder `telegram_bot/guide.pdf`.
    *   [x] Create `telegram_bot/bot.py` (initial structure started).
    *   [x] Create `telegram_bot/requirements.txt`.
*   [ ] **Version Control:**
    *   [x] Initialize Git repository in the project root (`/Users/mikitakavaliou/projects/aribot` or a dedicated subfolder if preferred).
    *   [ ] Create a `.gitignore` file (e.g., for `__pycache__`, `.env`, virtual environment folders).
    *   [x] Make initial commit.
*   [ ] **Python Environment:**
    *   [ ] Set up a virtual environment (e.g., `python -m venv venv`).
    *   [ ] Activate the virtual environment.
*   [ ] **Dependencies:**
    *   [ ] Add `python-telegram-bot` to `requirements.txt`.
    *   [ ] Install dependencies: `pip install -r telegram_bot/requirements.txt`.
*   [ ] **Telegram Bot Setup:**
    *   [ ] Create the bot using BotFather on Telegram.
    *   [ ] Obtain the **Bot Token**.
    *   [ ] Set the bot's name (using suggestions from the description doc).
*   [ ] **Configuration:**
    *   [ ] Decide on configuration method (environment variables recommended, or a config file).
    *   [ ] Securely store/set the `BOT_TOKEN`.
    *   [ ] Define `ADMIN_USER_IDS` (comma-separated string of admin Telegram User IDs).
    *   [ ] Define `[Your Topic]` placeholder value.
    *   [ ] Decide on persistence method for the guide reference (e.g., simple text file, JSON file, database). Create placeholder if needed (e.g., `guide_config.json`).

---

## Phase 2: Core Bot Development (`telegram_bot/bot.py`)

*   [ ] **Basic Application Setup:**
    *   [ ] Import necessary libraries (`os`, `json`, `logging`, `telegram`, `telegram.ext`).
    *   [ ] Set up basic logging configuration.
    *   [ ] Load configuration (token, admin IDs).
    *   [ ] Implement logic to load the current guide reference (file_id/URL) from persistence on startup.
    *   [ ] Create the `telegram.ext.Application` instance.
*   [ ] **`/start` Command Handler:**
    *   [ ] Implement the `start` function.
    *   [ ] Construct the welcome message using text from the description doc (Phase 2, Item 2).
    *   [ ] Create the `InlineKeyboardMarkup` with the "Get Guide" button (callback data: `get_guide`).
    *   [ ] Send the welcome message with the inline button.
    *   [ ] Register the `CommandHandler` for "start".
*   [ ] **Button Callback Handler:**
    *   [ ] Implement the `button_callback` function.
    *   [ ] Register the `CallbackQueryHandler`.
    *   [ ] Answer the callback query (`query.answer(...)`) for responsiveness.
    *   [ ] Check if `callback_data` is `get_guide`.
*   [ ] **Provide Guide Logic:**
    *   [ ] Inside the callback handler, get `user_id`.
    *   [ ] Retrieve the currently stored guide reference (file_id or URL) from memory/persistence.
    *   [ ] Construct the success message (Phase 2, Item 3 - Message 1).
    *   [ ] Send the success message.
    *   [ ] If a `file_id` is stored, use `context.bot.send_document(chat_id=user_id, document=stored_file_id)`.
    *   [ ] If a URL is stored, send a message containing the URL.
    *   [ ] Handle the case where no guide has been set yet by the admin.
*   [ ] **Error Handling:**
    *   [ ] Implement specific error handling within the `try...except` block for potential API errors.
    *   [ ] Log errors effectively.
    *   [ ] Send user-friendly error messages when appropriate (e.g., "Sorry, an error occurred...").
*   [ ] **Admin Command Handler (`/setguide`):**
    *   [ ] Implement the `set_guide` function.
    *   [ ] Register the `CommandHandler` for "setguide".
    *   [ ] Implement admin check: Verify `update.effective_user.id` is in the configured `ADMIN_USER_IDS`. Reject if not.
    *   [ ] **Method 1 (File ID):**
        *   [ ] Check if the command message is a reply (`update.message.reply_to_message`).
        *   [ ] Check if the replied-to message contains a document (`reply_to_message.document`).
        *   [ ] Check if the document is a PDF (check `mime_type` or filename extension).
        *   [ ] Extract the `file_id` (`reply_to_message.document.file_id`).
        *   [ ] Store the `file_id` persistently (overwrite previous value).
        *   [ ] Send confirmation message to admin.
    *   [ ] **Method 2 (URL):**
        *   [ ] Check if the command has arguments (`context.args`).
        *   [ ] Validate if the argument looks like a URL (basic check).
        *   [ ] Store the URL persistently (overwrite previous value).
        *   [ ] Send confirmation message to admin.
    *   [ ] **Error Handling:** Implement checks and messages for incorrect usage (no reply/args, not PDF, not admin) as per the description doc.
*   [ ] **Persistence Logic:**
    *   [ ] Implement functions to save the guide reference (file_id/URL) to the chosen persistent storage (e.g., writing to `guide_config.json`).
    *   [ ] Implement function to load the guide reference on bot startup.
*   [ ] **Logging:**
    *   [ ] Add informative log messages for key events (start, button click, errors, admin commands).

---

## Phase 3: Refinement & Testing

*   [ ] **Code Review & Cleanup:**
    *   [ ] Ensure all placeholders (`[Your Topic]`, etc.) are correctly replaced or loaded from config.
    *   [ ] Review code for clarity, efficiency, and adherence to Python best practices.
    *   [ ] Add comments where necessary.
*   [ ] **Functional Testing (Manual):**
    *   [ ] Test `/start` command: Does the welcome message and button appear correctly?
    *   [ ] Test user flow when a guide is set: Click the button, does the guide appear?
    *   [ ] Test user flow when no guide has been set yet by the admin yet.
*   [ ] **Admin Command Testing:**
    *   [ ] Test `/setguide` by replying to a PDF: Does it store the file_id and confirm?
    *   [ ] Test `/setguide <URL>`: Does it store the URL and confirm?
    *   [ ] Test `/setguide` by non-admin: Is it rejected?
    *   [ ] Test `/setguide` with incorrect usage (no reply/URL, reply to non-PDF): Are the correct error messages shown?
    *   [ ] After setting a guide (PDF/URL), test the normal user flow again: Is the *correct* guide sent?
    *   [ ] Test setting a PDF, then setting a URL, then setting another PDF: Does it correctly switch between methods?
*   [ ] **Persistence Testing:**
    *   [ ] Set a guide using `/setguide`.
    *   [ ] Restart the bot.
    *   [ ] Test the user flow: Does the bot remember and send the previously set guide?
*   [ ] **Edge Case Testing:**
    *   [ ] Test rapid button clicks.
*   [ ] **Error Message Testing:**
    *   [ ] Simulate error conditions (if possible) to verify user-facing error messages.
*   [ ] **Logging Verification:**
    *   [ ] Run the bot and check if logs capture the expected information and errors.

---

## Phase 4: Deployment (Production)

*   [ ] **Choose Hosting:**
    *   [ ] Select a hosting platform (e.g., VPS, Heroku, Render, PythonAnywhere, AWS Lambda/Google Cloud Functions). Consider cost, scalability, and ease of use.
*   [ ] **Prepare Environment:**
    *   [ ] Set up the production environment (install Python, Git).
    *   [ ] Clone the Git repository.
    *   [ ] Set up a production virtual environment.
    *   [ ] Install dependencies (`pip install -r telegram_bot/requirements.txt`).
    *   [ ] Configure **production** environment variables/config file (BOT_TOKEN, ADMIN_USER_IDS). **Do not commit sensitive data.**
    *   [ ] Ensure the persistence file/mechanism is correctly set up with appropriate permissions in production.
*   [ ] **Process Management:**
    *   [ ] If using a VPS/server, configure a process manager (like `systemd` or `supervisor`) to:
        *   Run the `bot.py` script.
        *   Automatically restart the bot if it crashes.
        *   Manage logs.
    *   [ ] If using a PaaS/FaaS, follow their specific deployment instructions.
*   [ ] **Deploy:**
    *   [ ] Push final code to Git remote (if applicable).
    *   [ ] Deploy the code to the hosting platform.
    *   [ ] Start the bot process.
*   [ ] **Final BotFather Configuration:**
    *   [ ] Use `/setdescription` to set the short description (from description doc).
    *   [ ] Use `/setabouttext` to set the about text (from description doc).
    *   [ ] Consider using `/setcommands` to list the `/start` command.
*   [ ] **Post-Deployment Check:**
    *   [ ] Perform basic functional tests on the live bot.
    *   [ ] Check production logs for any immediate errors.

---

## Phase 5: Maintenance & Monitoring

*   [ ] **Monitoring:**
    *   [ ] Set up basic uptime monitoring (if applicable to the hosting).
    *   [ ] Implement error monitoring/alerting (e.g., Sentry integration, or log monitoring).
*   [ ] **Logging:**
    *   [ ] Ensure logs are being collected and rotated appropriately.
    *   [ ] Periodically review logs for warnings or recurring errors.
*   [ ] **Updates:**
    *   [ ] Regularly update dependencies (`python-telegram-bot`, etc.) after testing.
    *   [ ] Keep the host system/environment updated.
*   [ ] **API Changes:**
    *   [ ] Stay informed about Telegram Bot API changes that might affect the bot's functionality.

---
