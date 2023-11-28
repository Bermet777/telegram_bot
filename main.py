import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# API key from OpenWeatherMap
API_KEY = "9ee30c3d4c072a847cde3cc1d93817b5"


# Define function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to the weather bot. Send me your latitude and longitude coordinates.")


# Define function to handle user messages
def get_weather(update, context):
    # Extract latitude and longitude coordinates from user message
    try:
        lat, lon = update.message.text.split(",")
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Invalid input. Please send your latitude and longitude as two comma-separated values.")
        return

    # API request URL
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"

    # Send API request and get response
    response = requests.get(url)

    # Parse JSON response into a dictionary
    data = response.json()

    # Extract weather information from dictionary
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]

    # Send weather information back to user
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Temperature: {temp:.1f}°C\nDescription: {description.capitalize()}")



# Create the updater and dispatcher
updater = Updater (token="6066026423:AAGClrZrJ1izJVOQW7uWe9a8oPZczbNYBO0", use_context=True)
dispatcher = updater.dispatcher

# Define the handlers
start_handler = CommandHandler('start', start)
weather_handler = MessageHandler(Filters.text & ~Filters.command, get_weather)

# Add the handlers to the dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(weather_handler)

# Start the bot
updater.start_polling()
updater.idle()
