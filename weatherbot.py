import telebot
import requests
from geopy.geocoders import Nominatim

BOT_TOKEN = '7959302797:AAG61VdF1zHnrMireBeGyWA8bNoGliogtKg'

WEATHER_API_KEY = '4e05ec2aed59343312e4fdac8a07ae80'

WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather?'

LANG = 'ru'

UNITS = 'metric'

bot = telebot.TeleBot(BOT_TOKEN)

geolocator = Nominatim(user_agent="weather_bot")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! \nВведите название города, чтобы узнать погоду.')

@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city = message.text.strip()

    location = geolocator.geocode(city)
    if location:
        latitude = round(location.latitude, 2)
        longitude = round(location.longitude, 2)

    # Запрос к API сервиса погоды
    complete_url = WEATHER_API_URL + 'lat=' + str(latitude) + '&lon=' + str(longitude) + '&appid=' + WEATHER_API_KEY + '&units=' + UNITS + '&lang=' + LANG
    response = requests.get(complete_url, timeout=20)

    # Проверка успешности запроса
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature = main['temp']
        feels_like = main['feels_like']
        temp_min = main['temp_min']
        temp_max = main['temp_max']
        pressure = int(round(main['pressure'] // 1.333, 0))
        humidity = main['humidity']
        description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        wind_deg = data['wind']['deg']
        clouds_all = data['clouds']['all']

        # Формирование сообщения
        weather_message = f'Погода в городе {city}:\n'
        weather_message += f'Температура: {temperature} °C\n'
        weather_message += f'Ощущается как: {feels_like} °C\n'
        weather_message += f'Минимальная суточная температура: {temp_min} °C\n'
        weather_message += f'Максимальная суточная температура: {temp_max} °C\n'
        weather_message += f'Давление: {pressure} мм рт. ст.\n'
        weather_message += f'Влажность: {humidity}%\n'
        weather_message += f'{description.capitalize()}\n'
        weather_message += f'Скорость ветра: {wind_speed} м/с\n'
        weather_message += f'Направление ветра: {wind_deg}°\n'
        weather_message += f'Облачность: {clouds_all}%\n'

        bot.send_message(message.chat.id, weather_message)

    else:
        bot.send_message(message.chat.id, 'Извините, я не смог получить данные о погоде. Пожалуйста, проверьте правильность введенного города.')

# Запуск бота
bot.polling()