# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
# It's located inside the telegram_bot directory in your project
COPY ./telegram_bot/requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir reduces image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire telegram_bot directory content into the container at /app/telegram_bot
# This includes bot.py and guide_config.json
COPY ./telegram_bot /app/telegram_bot

# Define environment variables placeholders (Best practice is to set these at runtime)
# ENV TELEGRAM_BOT_TOKEN=your_token_here
# ENV ADMIN_USER_IDS=your_admin_ids_here
# ENV GUIDE_TOPIC="Your Topic"
# ENV TARGET_CHANNEL_USERNAME="@YourChannelUsername" # Optional, remove if not used

# Run bot.py when the container launches
# The script `bot.py` uses the path "telegram_bot/guide_config.json"
# Since WORKDIR is /app, this command correctly executes /app/telegram_bot/bot.py
# and the script correctly finds /app/telegram_bot/guide_config.json
CMD ["python", "telegram_bot/bot.py"]