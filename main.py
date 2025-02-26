import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Get API keys from environment variables
API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not API_KEY or not BOT_TOKEN:
    raise ValueError("API_KEY and BOT_TOKEN must be set as environment variables.")


# Define function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Weather Bot! Send me your latitude and longitude as comma-separated values, for example, '37.7749,-122.4194'."
    )


# Define function to handle user messages
async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Extract latitude and longitude
        lat, lon = update.message.text.strip().split(",")
        lat = float(lat.strip())
        lon = float(lon.strip())
    except ValueError:
        await update.message.reply_text(
            "Invalid input! Please send as two comma-separated values, e.g., '37.7749,-122.4194'."
        )
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
            await update.message.reply_text(
                f"Weather in {city}:\nTemperature: {temp:.1f}°C\nDescription: {description.capitalize()}"
            )
        else:
            await update.message.reply_text(
                "Unable to fetch weather data. Please check your coordinates and try again."
            )
    except requests.RequestException as e:
        await update.message.reply_text(
            "Error fetching data from the weather service. Please try again later."
        )
        print(f"Error: {e}")


# Define a /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "This bot provides weather updates. Send latitude and longitude as comma-separated values, e.g., '37.7749,-122.4194'."
    )


# Handle unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sorry, I didn't understand that command. Type /help for assistance."
    )


# Create the application and handlers
app = Application.builder().token(BOT_TOKEN).build()

# Add handlers
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('help', help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))
app.add_handler(MessageHandler(filters.COMMAND, unknown))  # Catch unknown commands

# Start the bot
if __name__ == "__main__":
    app.run_polling()
