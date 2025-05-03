# Telegram Bot: Subscriber-Only Guide Access

This document outlines the specifications for a Telegram bot designed to provide a guide link exclusively to subscribers of a designated channel.

## Important Prerequisites

*   The bot **MUST** be added as an **administrator** to the target channel (`@[YourChannelUsername]`). It requires the "Can manage chat" permission or equivalent ability to view the member list.
*   The **Chat ID** or **Username** (e.g., `@YourChannelUsername`) of the target channel must be known and configured in the bot.
*   The **User ID** of the bot administrator(s) must be known and configured for admin commands.

## 1. Bot Name Suggestions (`/setname` in BotFather)

*   [Your Channel] Guide Bot
*   Subscriber Guide Access
*   [Your Topic] Guide (For Subs)
*   Verified Guide Access

## 2. Welcome Message (`/start` command)

*(Presents a button to initiate the process)*

*   **Message:**
    "Hello! 👋 This bot provides the **[Your Topic] Guide**, exclusively for subscribers of **@[YourChannelUsername]**.\n\n➡️ Click the button below to verify your subscription and get the guide.\n\n*If you haven't subscribed yet, please join **@[YourChannelUsername]** first, then click the button.*"
*   **Inline Keyboard Button:**
    *   Text: `✅ Verify Subscription & Get Guide`
    *   Callback Data: `check_subscription` (or similar identifier)

## 3. Bot Reply Logic (User clicks the 'Verify Subscription & Get Guide' button)

*   **STEP 1: Check Subscription Status (Triggered by Callback Query)**
    *   The bot receives a callback query with data `check_subscription` (or the identifier set on the button).
    *   The bot uses the Telegram Bot API's `getChatMember` method to check if the user (identified by their user ID from the callback query) is a member of the target channel (`@[YourChannelUsername]`).
    *   *(Optional but recommended)* The bot should answer the callback query (e.g., with a brief "Checking..." notification) to provide feedback to the user that the button press was registered.

*   **STEP 2 (Scenario A): User IS Subscribed**
    *   **Action:** The bot retrieves the currently configured guide reference (e.g., a PDF `file_id` or a URL).
    *   **Message 1:** "Great! Thanks for being a subscriber of **@[YourChannelUsername]**! ✅"
    *   **Message 2 (Option PDF):** Sends the configured PDF file directly to the user.
    *   **Message 2 (Option Link):** "Here is the guide link you requested:\n[Stored Guide Link Here]"

*   **STEP 2 (Scenario B): User IS NOT Subscribed**
    *   **Message:** "Access denied! ❌\n\nIt looks like you haven't joined our channel **@[YourChannelUsername]** yet.\n\nPlease subscribe here first: **@[YourChannelUsername]** [Optional: Add full t.me/YourChannelUsername link]\n\nOnce you've joined, come back and click the 'Verify Subscription & Get Guide' button again!"

## 4. Short Description (`/setdescription` in BotFather)

*   Sends the [Topic] guide to @[YourChannelUsername] subscribers.
*   Guide link for subscribers only.
*   Verify subscription via button & get the [Topic] guide.
*   Exclusive guide access for channel members (via button).

## 5. About Text (`/setabouttext` in BotFather)

*   **Option A (Clear Process with Button):**
    "This bot provides the **[Your Topic] Guide** exclusively for subscribers of **@[YourChannelUsername]**. \n\n**How to get the guide:**\n1. Ensure you are subscribed to **@[YourChannelUsername]**.\n2. Start this bot (or type `/start`).\n3. Click the 'Verify Subscription & Get Guide' button.\n4. The bot will check if you're a member.\n5. If yes, you'll receive the link. If no, you'll be asked to subscribe first.\n\nJoin our channel: **@[YourChannelUsername]**"

*   **Option B (Focus on Exclusivity with Button):**
    "Welcome! Get exclusive access to the **[Your Topic] Guide**! This resource is only available to verified members of our Telegram channel: **@[YourChannelUsername]**.\n\nClick the button below to check your subscription status. If you're a member, the guide will be sent instantly. If not, please join **@[YourChannelUsername]** and try the button again!"

---

## 6. Admin Commands

*   **Purpose:** Allow designated admin(s) to set the guide file/link the bot distributes.
*   **Admin Identification:** The bot needs a configured list of admin User IDs. Commands from other users should be ignored or rejected.
*   **Command:** `/setguide`
    *   **Method 1 (Recommended: Using File ID):**
        1.  Admin uploads the desired PDF guide directly to the chat with the bot.
        2.  Admin replies to the uploaded PDF message with the command `/setguide`.
        3.  **Bot Action:** Extracts the `file_id` of the PDF from the replied-to message, stores this `file_id` persistently (e.g., in a simple file, database, or bot's context persistence if configured), and confirms the update to the admin.
        4.  **Bot Reply:** "✅ Guide updated successfully. I will now send this PDF to verified subscribers."
    *   **Method 2 (Using URL):**
        1.  Admin sends the command `/setguide <URL_to_PDF>`.
        2.  **Bot Action:** Stores the provided `<URL_to_PDF>` persistently and confirms the update.
        3.  **Bot Reply:** "✅ Guide link updated successfully. I will now send this link to verified subscribers."
    *   **Error Handling:**
        *   If `/setguide` is used without replying to a PDF (Method 1) or without a URL (Method 2): "Usage: Reply to a PDF message with `/setguide` or use `/setguide <URL>`."
        *   If the user is not a configured admin: "❌ Sorry, this command is only available to bot administrators."
        *   If the replied-to message doesn't contain a PDF document: "❌ Please reply to a PDF file message with `/setguide`."

---

**Note:** Remember to replace `[Your Topic]` and `@[YourChannelUsername]` with your specific details. The `[Your Guide Link Here]` placeholder is now replaced by a dynamic mechanism managed via the `/setguide` command. The core functionality relies on implementing `getChatMember` and the admin command logic.
