# Telegram Bot: Guide Access

This document outlines the specifications for a Telegram bot designed to provide a guide link.

## Important Prerequisites

*   The **User ID** of the bot administrator(s) must be known and configured for admin commands.

## 1. Bot Name Suggestions (`/setname` in BotFather)

*   [Your Topic] Guide Bot
*   Guide Access
*   [Your Topic] Guide
*   Verified Guide Access

## 2. Welcome Message (`/start` command)

*(Presents a button to initiate the process)*

*   **Message:**
    "Hello! 👋 This bot provides the **[Your Topic] Guide**.\n\n➡️ Click the button below to get the guide."
*   **Inline Keyboard Button:**
    *   Text: `✅ Get Guide`
    *   Callback Data: `get_guide` (or similar identifier)

## 3. Bot Reply Logic (User clicks the 'Get Guide' button)

*   **STEP 1: Handle Button Click (Triggered by Callback Query)**
    *   The bot receives a callback query with data `get_guide` (or the identifier set on the button).
    *   *(Optional but recommended)* The bot should answer the callback query (e.g., with a brief "Getting guide..." notification) to provide feedback to the user that the button press was registered.

*   **STEP 2: Provide Guide**
    *   **Action:** The bot retrieves the currently configured guide reference (e.g., a PDF `file_id` or a URL).
    *   **Message 1:** "Thanks for your interest! ✅"
    *   **Message 2 (Option PDF):** Sends the configured PDF file directly to the user.
    *   **Message 2 (Option Link):** "Here is the guide link you requested:\n[Stored Guide Link Here]"

## 4. Short Description (`/setdescription` in BotFather)

*   Sends the [Topic] guide.
*   Guide link via button.
*   Get the [Topic] guide via button.

## 5. About Text (`/setabouttext` in BotFather)

*   **Option A (Clear Process with Button):**
    "This bot provides the **[Your Topic] Guide**. \n\n**How to get the guide:**\n1. Start this bot (or type `/start`).\n2. Click the 'Get Guide' button.\n3. You'll receive the guide link or file."

*   **Option B (Focus on Guide Access with Button):**
    "Welcome! Get access to the **[Your Topic] Guide**! Click the button below to get the guide instantly."

---

## 6. Admin Commands

*   **Purpose:** Allow designated admin(s) to set the guide file/link the bot distributes.
*   **Admin Identification:** The bot needs a configured list of admin User IDs. Commands from other users should be ignored or rejected.
*   **Command:** `/setguide`
    *   **Method 1 (Recommended: Using File ID):**
        1.  Admin uploads the desired PDF guide directly to the chat with the bot.
        2.  Admin replies to the uploaded PDF message with the command `/setguide`.
        3.  **Bot Action:** Extracts the `file_id` of the PDF from the replied-to message, stores this `file_id` persistently (e.g., in a simple file, database, or bot's context persistence if configured), and confirms the update to the admin.
        4.  **Bot Reply:** "✅ Guide updated successfully. I will now send this PDF."
    *   **Method 2 (Using URL):**
        1.  Admin sends the command `/setguide <URL_to_PDF>`.
        2.  **Bot Action:** Stores the provided `<URL_to_PDF>` persistently and confirms the update.
        3.  **Bot Reply:** "✅ Guide link updated successfully. I will now send this link."
    *   **Error Handling:**
        *   If `/setguide` is used without replying to a PDF (Method 1) or without a URL (Method 2): "Usage: Reply to a PDF message with `/setguide` or use `/setguide <URL>`."
        *   If the user is not a configured admin: "❌ Sorry, this command is only available to bot administrators."
        *   If the replied-to message doesn't contain a PDF document: "❌ Please reply to a PDF file message with `/setguide`."

---

**Note:** Remember to replace `[Your Topic]` with your specific details. The `[Your Guide Link Here]` placeholder is now replaced by a dynamic mechanism managed via the `/setguide` command.
