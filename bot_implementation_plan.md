# Telegram Subscriber Bot - Implementation Plan

This document outlines the steps required to develop, test, and deploy the subscriber-only Telegram guide bot.

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
    *   [ ] Create `telegram_bot/bot.py` (initial structure started).
    *   [ ] Create `telegram_bot/requirements.txt`.
*   [ ] **Version Control:**
    *   [ ] Initialize Git repository in the project root (`/Users/mikitakavaliou/projects/aribot` or a dedicated subfolder if preferred).
    *   [ ] Create a `.gitignore` file (e.g., for `__pycache__`, `.env`, virtual environment folders).
    *   [ ] Make initial commit.
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
    *   [ ] Define `TARGET_CHANNEL_USERNAME` (e.g., `@YourChannelUsername`).
    *   [ ] Define `GUIDE_LINK` (the actual URL or method to get the guide).
    *   [ ] Define `[Your Topic]` placeholder value.
*   [ ] **Channel Integration:**
    *   [ ] Add the created bot as an **administrator** to the target Telegram channel.
    *   [ ] Ensure the bot has permission to "manage chat" or at least view members.

---

## Phase 2: Core Bot Development (`telegram_bot/bot.py`)

*   [ ] **Basic Application Setup:**
    *   [ ] Import necessary libraries (`os`, `logging`, `telegram`, `telegram.ext`).
    *   [ ] Set up basic logging configuration.
    *   [ ] Load configuration (token, channel ID, guide link).
    *   [ ] Create the `telegram.ext.Application` instance.
*   [ ] **`/start` Command Handler:**
    *   [ ] Implement the `start` function.
    *   [ ] Construct the welcome message using text from the description doc (Phase 2, Item 2).
    *   [ ] Create the `InlineKeyboardMarkup` with the "Verify Subscription & Get Guide" button (callback data: `check_subscription`).
    *   [ ] Send the welcome message with the inline button.
    *   [ ] Register the `CommandHandler` for "start".
*   [ ] **Button Callback Handler:**
    *   [ ] Implement the `button_callback` function.
    *   [ ] Register the `CallbackQueryHandler`.
    *   [ ] Answer the callback query (`query.answer(...)`) for responsiveness.
    *   [ ] Check if `callback_data` is `check_subscription`.
*   [ ] **Subscription Check Logic:**
    *   [ ] Inside the callback handler, get `user_id` and `chat_id` (`TARGET_CHANNEL_USERNAME`).
    *   [ ] Call `context.bot.get_chat_member(chat_id=TARGET_CHANNEL_USERNAME, user_id=user_id)`.
    *   [ ] Use a `try...except` block to handle potential `telegram.error.BadRequest` and other exceptions.
*   [ ] **Handle Subscribed User:**
    *   [ ] Check if `member.status` is `member`, `administrator`, or `creator`.
    *   [ ] Construct the success message (Phase 2, Item 3, Scenario A).
    *   [ ] Send the success message with the `GUIDE_LINK`. (Decide: edit original message or send new one).
*   [ ] **Handle Non-Subscribed User:**
    *   [ ] Handle cases where `member.status` is `left`, `kicked`, or the `get_chat_member` call fails with "user not found".
    *   [ ] Construct the denial message (Phase 2, Item 3, Scenario B).
    *   [ ] Send the denial message.
*   [ ] **Error Handling:**
    *   [ ] Implement specific error handling within the `try...except` block for:
        *   Bot not admin / chat not found (`BadRequest`).
        *   User not found (`BadRequest`).
        *   Other potential API errors.
    *   [ ] Log errors effectively.
    *   [ ] Send user-friendly error messages when appropriate (e.g., "Sorry, an error occurred...").
*   [ ] **Logging:**
    *   [ ] Add informative log messages for key events (start, button click, subscription check result, errors).

---

## Phase 3: Refinement & Testing

*   [ ] **Code Review & Cleanup:**
    *   [ ] Ensure all placeholders (`[Your Topic]`, etc.) are correctly replaced or loaded from config.
    *   [ ] Review code for clarity, efficiency, and adherence to Python best practices.
    *   [ ] Add comments where necessary.
*   [ ] **Functional Testing (Manual):**
    *   [ ] Test `/start` command: Does the welcome message and button appear correctly?
    *   [ ] Test Scenario A (Subscribed): Join the channel, start the bot, click the button. Does the success message and link appear?
    *   [ ] Test Scenario B (Not Subscribed): Leave the channel (or use an account that hasn't joined), start the bot, click the button. Does the denial message appear?
    *   [ ] Test joining *after* clicking the button while unsubscribed, then clicking again.
*   [ ] **Edge Case Testing:**
    *   [ ] Test with a user who has never interacted with the channel.
    *   [ ] Test what happens if the bot is removed as admin from the channel.
    *   [ ] Test with an invalid `TARGET_CHANNEL_USERNAME`.
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
    *   [ ] Configure **production** environment variables (BOT_TOKEN, TARGET_CHANNEL_USERNAME, GUIDE_LINK). **Do not commit sensitive data.**
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
