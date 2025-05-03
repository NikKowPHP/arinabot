i6mport os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Load configuration from environment variables
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TARGET_CHANNEL_USERNAME = os.environ.get("TARGET_CHANNEL_USERNAME", "") # Make TARGET_CHANNEL_USERNAME optional
ADMIN_USER_IDS = os.environ["ADMIN_USER_IDS"].split(",")
GUIDE_CONFIG_FILE = "telegram_bot/guide_config.json"

# --- Logging Setup ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)  # Reduce httpx verbosity
logger = logging.getLogger(__name__)

# --- Load Guide Configuration ---
def load_guide_config():
    try:
        with open(GUIDE_CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("guide_reference"), config.get("reference_type")
    except FileNotFoundError:
        logger.warning(f"Guide config file not found: {GUIDE_CONFIG_FILE}. Using default (None).")
        return None, None
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {GUIDE_CONFIG_FILE}. Check file contents.")
        return None, None

# --- Save Guide Configuration ---
def save_guide_config(guide_reference, reference_type):
    try:
        with open(GUIDE_CONFIG_FILE, "w") as f:
            json.dump({"guide_reference": guide_reference, "reference_type": reference_type}, f)
    except Exception as e:
        logger.error(f"Error saving guide config to {GUIDE_CONFIG_FILE}: {e}")

# Load initial guide reference from file
GUIDE_REFERENCE, REFERENCE_TYPE = load_guide_config()

# --- Admin Check ---
def is_admin(user_id: int) -> bool:
    return str(user_id) in ADMIN_USER_IDS

# --- Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the welcome message with the verification button."""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot.")

    welcome_text = (
        f"Hello! 👋 This bot provides the **[Your Topic] Guide**, exclusively for subscribers of **{TARGET_CHANNEL_USERNAME}**.\n\n"
        f"➡️ Click the button below to verify your subscription and get the guide.\n\n"
        f"*If you haven't subscribed yet, please join **{TARGET_CHANNEL_USERNAME}** first, then click the button.*"
    )

    keyboard = [
        [InlineKeyboardButton("✅ Verify Subscription & Get Guide", callback_data="check_subscription")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the button click (callback query)."""
    query = update.callback_query
    user_id = query.from_user.id
    username = query.from_user.username
    callback_data = query.data

    logger.info(f"Received callback query from user {user_id} ({username}) with data: {callback_data}")

    # Answer the callback query to remove the "loading" state on the button
    await query.answer("Checking subscription...")

    if callback_data == "check_subscription":
        # The channel membership check has been removed as per user request.
        # The bot will now send the guide to anyone who clicks the button.

        await query.message.reply_text("Thanks for your interest! ✅", parse_mode=ParseMode.MARKDOWN)

        if GUIDE_REFERENCE:
            if REFERENCE_TYPE == "file_id":
                try:
                    await context.bot.send_document(chat_id=user_id, document=GUIDE_REFERENCE)
                except Exception as e:
                    logger.error(f"Error sending document to user {user_id}: {e}")
                    await query.message.reply_text("Sorry, there was an error sending the guide. Please contact the administrator.", parse_mode=ParseMode.MARKDOWN)

            elif REFERENCE_TYPE == "url":
                await query.message.reply_text(f"Here is the guide link you requested:\n{GUIDE_REFERENCE}", parse_mode=ParseMode.MARKDOWN)
            else:
                logger.warning(f"Invalid REFERENCE_TYPE: {REFERENCE_TYPE}")
                await query.message.reply_text("Sorry, the guide is currently unavailable. Please contact the administrator.", parse_mode=ParseMode.MARKDOWN)
        else:
            logger.info("No guide has been set yet.")
            await query.message.reply_text("Sorry, the guide is currently unavailable. Please contact the administrator.", parse_mode=ParseMode.MARKDOWN)

    else:
        logger.warning(f"Received unknown callback data: {callback_data}")
        await query.answer("Unknown action.")

async def set_guide(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allows an admin to set the guide file (PDF) or link."""
    user = update.effective_user
    if not is_admin(user.id):
        await update.message.reply_text("❌ Sorry, this command is only available to bot administrators.")
        return

    if update.message.reply_to_message:
        # Method 1: Using File ID
        if update.message.reply_to_message.document:
            document = update.message.reply_to_message.document
            if document.mime_type == "application/pdf" or document.file_name.endswith(".pdf"):
                file_id = document.file_id
                save_guide_config(file_id, "file_id")
                GUIDE_REFERENCE = file_id
                REFERENCE_TYPE = "file_id"
                await update.message.reply_text("✅ Guide updated successfully. I will now send this PDF to verified subscribers.")
                logger.info(f"Admin {user.id} set guide to file_id: {file_id}")
            else:
                await update.message.reply_text("❌ Please reply to a PDF file message with `/setguide`.")
        else:
            await update.message.reply_text("❌ Please reply to a PDF file message with `/setguide`.")
    elif context.args:
        # Method 2: Using URL
        url = context.args[0]
        # Basic URL validation (can be improved)
        if url.startswith("http://") or url.startswith("https://"):
            save_guide_config(url, "url")
            GUIDE_REFERENCE = url
            REFERENCE_TYPE = "url"
            await update.message.reply_text("✅ Guide link updated successfully. I will now send this link to verified subscribers.")
            logger.info(f"Admin {user.id} set guide to URL: {url}")
        else:
            await update.message.reply_text("❌ Please provide a valid URL with `/setguide <URL>`.")
    else:
        await update.message.reply_text("Usage: Reply to a PDF message with `/setguide` or use `/setguide <URL>`.")

def main() -> None:
    """Start the bot."""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TARGET_CHANNEL_USERNAME == "@YourChannelUsername":
        logger.warning("Please replace placeholders for BOT_TOKEN and TARGET_CHANNEL_USERNAME in the script or set environment variables.")
        # You might want to exit here if configuration is missing
        # return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CommandHandler("setguide", set_guide))

    # Add error handler (optional but recommended)
    # application.add_error_handler(error_handler) # Define an error_handler function if needed

    logger.info("Starting bot polling...")
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
