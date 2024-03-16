from telebot import TeleBot, types
import requests

TOKEN = '6942161053:AAEjC-ISg8LwY5U5V2xB9oOzxZL3NF3VQ4Y'

API_KEY = '3a2127fa2f3f7e79cb112469e51ad4a9'

URL_WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather'

bot = TeleBot(TOKEN)

EMOJI_CODE = {
    '01d': '☀️',
    '02d': '⛅',
    '03d': '☁️',
    '04d': '🌧️',
    '09d': '🌧️',
    '10d': '🌦️',
    '11d': '🌩️',
    '13d': '❄️',
    '50d': '🌫️',
    '01n': '🌕',
    '02n': '⛅',
    '03n': '☁️',
    '04n': '🌧️',
    '09n': '🌧️',
    '10n': '🌦️',
    '11n': '🌩️',
    '13n': '❄️',
    '50n': '🌫️',
}

def get_weather(lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
        'lang': 'ru',
        'units': 'metric',
        'appid': API_KEY
    }

    response = requests.get(URL_WEATHER_API, params=params).json()

    city_name = response['name']
    description = response['weather'][0]['description']
    code = response['weather'][0]['icon']
    temp = response['main']['temp']
    temp_feels_like = response['main']['feels_like']
    humidity = response['main']['humidity']

    return f'🌆 {city_name}\n' \
           f'🌤️ {description}\n' \
           f'🌡️ {temp}°C (ощущается как {temp_feels_like}°C)\n' \
           f'💧 Влажность: {humidity}%'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Отправь мне свое местоположение и я отправлю тебе погоду.', request_location=True)
    keyboard.add(button)

    bot.send_message(message.chat.id, 'Привет! Нажми кнопку и отправь мне свое местоположение.', reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon = message.location.longitude
    lat = message.location.latitude

    result = get_weather(lat, lon)

    bot.send_message(message.chat.id, result, reply_markup=keyboard)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button = types.KeyboardButton('О проекте')
button2 = types.KeyboardButton('Отправь мне свое местоположение и я отправлю тебе погоду.', request_location=True)
keyboard.add(button, button2)

@bot.message_handler(func=lambda message: message.text == 'О проекте')
def send_about(message):
    bot.send_message(message.chat.id, 'Этот бот предназначен для получения текущей погоды.', reply_markup=keyboard)

bot.infinity_polling()


