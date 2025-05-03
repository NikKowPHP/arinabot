# Telegram Bot: Subscriber-Only Guide Access

This document outlines the specifications for a Telegram bot designed to provide a guide link exclusively to subscribers of a designated channel.

## Important Prerequisites

*   The bot **MUST** be added as an **administrator** to the target channel (`@[YourChannelUsername]`). It requires the "Can manage chat" permission or equivalent ability to view the member list.
*   The **Chat ID** or **Username** (e.g., `@YourChannelUsername`) of the target channel must be known and configured in the bot.

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
    *   **Message:** "Great! Thanks for being a subscriber of **@[YourChannelUsername]**! ✅\n\nHere is the guide link you requested:\n[Your Guide Link Here]"
    *   *(Optional alternative - two messages)*
        *   *Message 1:* "Subscription confirmed! Thanks for being part of **@[YourChannelUsername]**! 👍"
        *   *Message 2:* "Here's your guide:\n[Your Guide Link Here]"

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
    "Welcome! Get exclusive access to the **[Your Topic] Guide**! This resource is only available to verified members of our Telegram channel: **@[YourChannelUsername]**.\n\nClick the button below to check your subscription status. If you're a member, the link will be sent instantly. If not, please join **@[YourChannelUsername]** and try the button again!"

---

**Note:** Remember to replace `[Your Topic]`, `@[YourChannelUsername]`, and `[Your Guide Link Here]` with your specific details when configuring the bot. The core functionality relies on the correct implementation of the `getChatMember` API call.
