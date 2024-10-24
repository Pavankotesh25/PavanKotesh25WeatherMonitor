import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt
import sqlite3

API_KEY = 'c2f811cd067bb0bd4e495d30d41c21e9'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
INTERVAL = 300  # 5 minutes in seconds
ALERT_THRESHOLD = 35.0  # 35 degrees Celsius

daily_data = {}

def fetch_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)
    return response.json()

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def update_daily_summary(city, weather_data):
    date = datetime.utcfromtimestamp(weather_data['dt']).date()
    temp = kelvin_to_celsius(weather_data['main']['temp'])
    feels_like = kelvin_to_celsius(weather_data['main']['feels_like'])
    main = weather_data['weather'][0]['main']
    
    if date not in daily_data:
        daily_data[date] = {'temps': [], 'feels_likes': [], 'conditions': []}

    daily_data[date]['temps'].append(temp)
    daily_data[date]['feels_likes'].append(feels_like)
    daily_data[date]['conditions'].append(main)

def init_db():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS daily_summaries
                      (date TEXT, avg_temp REAL, max_temp REAL, min_temp REAL, dominant_condition TEXT)''')
    conn.commit()
    conn.close()

def store_daily_summary(date, avg_temp, max_temp, min_temp, dominant_condition):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO daily_summaries (date, avg_temp, max_temp, min_temp, dominant_condition)
                      VALUES (?, ?, ?, ?, ?)''', (date, avg_temp, max_temp, min_temp, dominant_condition))
    conn.commit()
    conn.close()

def calculate_daily_summary():
    for date, data in daily_data.items():
        avg_temp = sum(data['temps']) / len(data['temps'])
        max_temp = max(data['temps'])
        min_temp = min(data['temps'])
        dominant_condition = max(set(data['conditions']), key=data['conditions'].count)
        
        store_daily_summary(date, avg_temp, max_temp, min_temp, dominant_condition)
        
        print(f"Date: {date}")
        print(f"Average Temp: {avg_temp:.2f}°C")
        print(f"Max Temp: {max_temp:.2f}°C")
        print(f"Min Temp: {min_temp:.2f}°C")
        print(f"Dominant Condition: {dominant_condition}\n")

def check_alerts(city, temp):
    if temp > ALERT_THRESHOLD:
        print(f"Alert! Temperature in {city} has exceeded {ALERT_THRESHOLD}°C")

def plot_daily_summary():
    dates = list(daily_data.keys())
    avg_temps = [sum(data['temps']) / len(data['temps']) for data in daily_data.values()]

    plt.plot(dates, avg_temps, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Average Temperature (°C)')
    plt.title('Daily Average Temperature')
    plt.show()

def fetch_daily_summaries():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM daily_summaries''')
    rows = cursor.fetchall()
    conn.close()
    return rows

init_db()

while True:
    for city in CITIES:
        weather_data = fetch_weather_data(city)
        print(weather_data)  # For now, we just print the data. We'll process it later.
        update_daily_summary(city, weather_data)
        temp = kelvin_to_celsius(weather_data['main']['temp'])
        check_alerts(city, temp)
    calculate_daily_summary()
    plot_daily_summary()
    time.sleep(INTERVAL)

# Fetch and display stored summaries
summaries = fetch_daily_summaries()

for summary in summaries:
    date, avg_temp, max_temp, min_temp, dominant_condition = summary
    print(f"Date: {date}")
    print(f"Average Temp: {avg_temp:.2f}°C")
    print(f"Max Temp: {max_temp:.2f}°C")
    print(f"Min Temp: {min_temp:.2f}°C")
    print(f"Dominant Condition: {dominant_condition}\n")
