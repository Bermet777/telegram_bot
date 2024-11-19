import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Get API keys from environment variables
API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")


# Define function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to the Weather Bot! Send me your latitude and longitude as comma-separated values, e.g., '37.7749,-122.4194'.")


# Define function to handle user messages
def get_weather(update, context):
    try:
        # Extract latitude and longitude
        lat, lon = update.message.text.strip().split(",")
        lat = float(lat.strip())
        lon = float(lon.strip())
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Invalid input! Please send your latitude and longitude as two comma-separated values, e.g., '37.7749,-122.4194'.")
        return

    # API request URL
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP errors
        data = response.json()

        # Check if the response contains weather data
        if "main" in data and "weather" in data:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            city = data.get("name", "Unknown location")

            # Send weather information back to user
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Weather in {city}:\nTemperature: {temp:.1f}°C\nDescription: {description.capitalize()}")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Unable to fetch weather data. Please check your coordinates and try again.")
    except requests.RequestException as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Error fetching data from the weather service. Please try again later.")
        print(f"Error: {e}")


# Define a /help command
def help_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="This bot provides weather updates. Send latitude and longitude as comma-separated values, e.g., '37.7749,-122.4194'.")


# Handle unknown commands
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command. Type /help for assistance.")


# Create the updater and dispatcher
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define the handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help_command))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_weather))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))  # Catch unknown commands

# Start the bot
if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
