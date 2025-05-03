import os
import json
import logging
import asyncio # Import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, TypeHandler # Add TypeHandler
from telegram.error import BadRequest, Conflict # Keep Conflict for potential webhook setup issues
from dotenv import load_dotenv
import traceback
from telegram.helpers import escape_markdown
import html # Need html for escaping in error handler

# --- Webhook specific imports ---
from aiohttp import web

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ADMIN_USER_IDS = os.environ["ADMIN_USER_IDS"].split(",")
GUIDE_CONFIG_FILE = "telegram_bot/guide_config.json"
GUIDE_TOPIC = os.environ.get("GUIDE_TOPIC", "Default Topic")
# --- Webhook Configuration ---
# Get PORT from environment variable provided by Cloud Run
PORT = int(os.environ.get("PORT", 8080))
# You NEED a publicly accessible HTTPS URL for your Cloud Run service
# Set this via environment variable during deployment or hardcode TEMPORARILY for testing
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "YOUR_CLOUDRUN_SERVICE_HTTPS_URL_HERE/webhook")
WEBHOOK_SECRET_TOKEN = os.environ.get("WEBHOOK_SECRET_TOKEN", "YOUR_SECRET_RANDOM_STRING") # Optional but recommended

# --- Logging Setup ---
# (Keep your existing logging setup)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# --- Load/Save Guide Configuration (Keep as is) ---
def load_guide_config():
    # ... (your existing function) ...
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

def save_guide_config(guide_reference, reference_type):
     # ... (your existing function) ...
    try:
        with open(GUIDE_CONFIG_FILE, "w") as f:
            json.dump({"guide_reference": guide_reference, "reference_type": reference_type}, f)
    except Exception as e:
        logger.error(f"Error saving guide config to {GUIDE_CONFIG_FILE}: {e}")

GUIDE_REFERENCE, REFERENCE_TYPE = load_guide_config()

# --- Admin Check (Keep as is) ---
def is_admin(user_id: int) -> bool:
     # ... (your existing function) ...
     return str(user_id) in ADMIN_USER_IDS

# --- Bot Handlers (Keep your start, button_callback, set_guide handlers as they are) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing function) ...
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot via /start.")
    # Make sure TARGET_CHANNEL_USERNAME is defined or handled if missing
    target_channel = os.environ.get("TARGET_CHANNEL_USERNAME", "the channel") # Example fallback
    welcome_text = (
        f"Привет! 👋 Этот бот предоставляет **{GUIDE_TOPIC} Руководство**, эксклюзивно для подписчиков **{target_channel}**.\n\n"
        f"➡️ Нажмите кнопку ниже, чтобы подтвердить подписку и получить руководство.\n\n"
        f"*Если вы еще не подписаны, пожалуйста, сначала присоединитесь к **{target_channel}**, затем нажмите кнопку.*"
    )
    keyboard = [
        [InlineKeyboardButton("✅ Подтвердить подписку и получить руководство", callback_data="check_subscription")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing function) ...
    query = update.callback_query
    user_id = query.from_user.id
    username = query.from_user.username
    callback_data = query.data
    logger.info(f"Received callback query from user {user_id} ({username}) with data: {callback_data}")
    await query.answer("Обработка...") # Change message slightly maybe

    if callback_data == "check_subscription":
        await query.message.reply_text("Спасибо за ваш интерес! ✅", parse_mode=ParseMode.MARKDOWN)
        # Load guide config *inside* the handler if it might change
        # guide_ref, ref_type = load_guide_config() # Or use global if you don't expect it to change often
        if GUIDE_REFERENCE: # Use the global variables loaded at start or re-load here
            if REFERENCE_TYPE == "file_id":
                try:
                    await context.bot.send_document(chat_id=user_id, document=GUIDE_REFERENCE)
                except Exception as e:
                    logger.error(f"Error sending document to user {user_id}: {e}")
                    await query.message.reply_text("Извините, произошла ошибка при отправке руководства. Пожалуйста, свяжитесь с администратором.", parse_mode=ParseMode.MARKDOWN)
            elif REFERENCE_TYPE == "url":
                escaped_guide_reference = escape_markdown(GUIDE_REFERENCE, version=2)
                await query.message.reply_text(f"Вот ссылка на руководство, которую вы запросили:\n{escaped_guide_reference}", parse_mode=ParseMode.MARKDOWN_V2)
            else:
                logger.warning(f"Invalid REFERENCE_TYPE: {REFERENCE_TYPE}")
                await query.message.reply_text("Извините, руководство в настоящее время недоступно. Пожалуйста, свяжитесь с администратором.", parse_mode=ParseMode.MARKDOWN)
        else:
            logger.info("No guide has been set yet.")
            await query.message.reply_text("Извините, руководство в настоящее время недоступно. Пожалуйста, свяжитесь с администратором.", parse_mode=ParseMode.MARKDOWN)
    else:
        logger.warning(f"Received unknown callback data: {callback_data}")
        await query.answer("Неизвестное действие.")


async def set_guide(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing function, ensure globals GUIDE_REFERENCE/REFERENCE_TYPE are updated) ...
    global GUIDE_REFERENCE, REFERENCE_TYPE # Declare modification of globals
    user = update.effective_user
    if not is_admin(user.id):
        await update.message.reply_text("❌ Извините, эта команда доступна только администраторам бота.")
        return

    if update.message.reply_to_message:
        if update.message.reply_to_message.document:
            document = update.message.reply_to_message.document
            if document.mime_type == "application/pdf" or (document.file_name and document.file_name.endswith(".pdf")):
                file_id = document.file_id
                save_guide_config(file_id, "file_id")
                GUIDE_REFERENCE = file_id # Update global
                REFERENCE_TYPE = "file_id" # Update global
                await update.message.reply_text("✅ Руководство (PDF) успешно обновлено.")
                logger.info(f"Admin {user.id} set guide to file_id: {file_id}")
            else:
                await update.message.reply_text("❌ Пожалуйста, ответьте на сообщение с PDF-файлом, используя `/setguide`.")
        else:
            await update.message.reply_text("❌ Пожалуйста, ответьте на сообщение с PDF-файлом, используя `/setguide`.")
    elif context.args:
        url = context.args[0]
        if url.startswith("http://") or url.startswith("https://"):
            save_guide_config(url, "url")
            GUIDE_REFERENCE = url # Update global
            REFERENCE_TYPE = "url" # Update global
            await update.message.reply_text("✅ Ссылка на руководство успешно обновлена.")
            logger.info(f"Admin {user.id} set guide to URL: {url}")
        else:
            await update.message.reply_text("❌ Пожалуйста, укажите действительный URL, используя `/setguide <URL>`.")
    else:
        await update.message.reply_text("Использование: Ответьте на сообщение с PDF, используя `/setguide`, или используйте `/setguide <URL>`.")


# --- Error Handler (Keep as is, ensure `html` is imported) ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (your existing function, ensure html is imported) ...
    logger.error("Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    for admin_id in ADMIN_USER_IDS:
        try:
            # Split message if too long
            MAX_MESSAGE_LENGTH = 4096
            for i in range(0, len(message), MAX_MESSAGE_LENGTH):
                 await context.bot.send_message(
                    chat_id=admin_id, text=message[i:i + MAX_MESSAGE_LENGTH], parse_mode=ParseMode.HTML
                )
        except Exception:
            logger.exception("Could not send exception details to admin %s", admin_id)


async def main() -> None:
    """Set up PTB application and aiohttp web server."""
    # --- PTB Application Setup ---
    # Don't pass webhook_url or listen here, we use aiohttp for that
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .read_timeout(30) # Increase timeouts if needed
        .write_timeout(30)
        .connect_timeout(30)
        .build()
    )

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CommandHandler("setguide", set_guide))
    # Optional: Add a TypeHandler to process incoming Updates from the webhook
    # This is often done within the web server handler itself
    application.add_error_handler(error_handler)

    # Initialize PTB application (important for webhook setup)
    await application.initialize()

    # Set the webhook only if WEBHOOK_URL is configured
    if "YOUR_CLOUDRUN_SERVICE_HTTPS_URL_HERE" not in WEBHOOK_URL:
        logger.info(f"Setting webhook to {WEBHOOK_URL}")
        try:
            await application.bot.set_webhook(
                url=WEBHOOK_URL,
                allowed_updates=Update.ALL_TYPES, # Specify which updates you want
                secret_token=WEBHOOK_SECRET_TOKEN # Pass the secret token
            )
            logger.info("Webhook set successfully")
        except Exception as e:
             logger.error(f"Failed to set webhook: {e}")
             # Decide if you want to exit or try to continue without webhook
             # return # Exit if webhook setup fails and is critical
    else:
        logger.warning("WEBHOOK_URL is not configured. Skipping webhook setup.")
        # If you skip setup, the bot won't receive messages via webhook!

    # --- aiohttp Web Server Setup ---
    async def telegram_webhook_handler(request: web.Request) -> web.Response:
        """Handles incoming Telegram updates via POST."""
        # Check secret token if configured (recommended)
        if WEBHOOK_SECRET_TOKEN:
            if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET_TOKEN:
                logger.warning("Invalid secret token received")
                return web.Response(status=403) # Forbidden

        try:
            update_data = await request.json()
            update = Update.de_json(update_data, application.bot)
            logger.debug(f"Received update via webhook: {update_data}")
            # Process the update via PTB's dispatcher
            await application.process_update(update)
            return web.Response(status=200) # OK
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from webhook request")
            return web.Response(status=400) # Bad Request
        except Exception as e:
            logger.error(f"Error processing webhook update: {e}", exc_info=True)
            return web.Response(status=500) # Internal Server Error

    # --- Health Check Endpoint (Required by Cloud Run) ---
    async def health_check_handler(request: web.Request) -> web.Response:
        """A simple health check endpoint."""
        # You could add checks here, e.g., application.bot.get_me() if needed
        return web.Response(text="OK", status=200)

    # Create aiohttp application
    aiohttp_app = web.Application()
    # Route for Telegram webhook (use a path component in your WEBHOOK_URL)
    webhook_path = "/" + WEBHOOK_URL.split('/')[-1] # e.g., "/webhook"
    aiohttp_app.router.add_post(webhook_path, telegram_webhook_handler)
    # Route for Cloud Run health checks
    aiohttp_app.router.add_get("/", health_check_handler) # Respond to '/' for basic health check

    # Create runner and site
    runner = web.AppRunner(aiohttp_app)
    await runner.setup()
    # Listen on 0.0.0.0 and the PORT from Cloud Run
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    logger.info(f"Starting web server on 0.0.0.0:{PORT}")
    await site.start()

    # Keep the application running (aiohttp handles the event loop)
    # We don't use application.run_polling() anymore
    # Keep PTB's background tasks running (like job_queue if you use it)
    await application.start()
    logger.info("PTB Application started (handlers ready). Web server is running.")
    # Keep the server running until interrupted
    await asyncio.Event().wait() # Keep running indefinitely

    # --- Cleanup (will likely only run on graceful shutdown) ---
    logger.info("Shutting down...")
    await application.stop()
    await runner.cleanup()
    await application.shutdown()
    logger.info("Shutdown complete.")


if __name__ == "__main__":
    # Ensure loop is created correctly if needed (usually handled by asyncio.run)
    # For simple cases, asyncio.run is fine
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
         logger.info("Bot stopped manually.")
    except Exception as e:
         logger.critical(f"Critical error causing bot to stop: {e}", exc_info=True)