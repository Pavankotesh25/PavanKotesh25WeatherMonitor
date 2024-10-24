# PavanKotesh25WeatherMonitor
Built a real-time weather monitoring system using the OpenWeatherMap API, gathering data for Indian metros at regular intervals. The system converts temperature from Kelvin to Celsius, calculates daily summaries including average, max, and min temperatures, and tracks dominant weather conditions. It supports custom alert thresholds for specific weather criteria and provides visualizations of weather data and alerts. All data is stored in a database for future analysis, with additional support for parameters like humidity and wind speed. Key features include error handling for invalid data.

Core Features:

Daily Summaries: Compute and store daily average, max, and min temperatures, along with the primary weather condition.
Alerts: Set custom thresholds (e.g., temperatures exceeding 35°C) and trigger notifications when conditions are met.
Visualizations: Present daily trends, summaries, and alerts graphically.
Testing Approach:

API Connectivity: Ensure a valid connection to the OpenWeatherMap API.
Data Simulation: Mock API calls to simulate real-time data.
Temperature Conversion: Verify the accuracy of temperature conversions.
Summaries: Test the accuracy of daily summaries.
Alert Functionality: Check alert triggers based on defined thresholds.
Python Script Output:

Weather Data Example (for Delhi, Mumbai, Chennai, Bengaluru, Kolkata, Hyderabad):
Location: Delhi, Temp: 299.2K, Condition: Haze
Mumbai: 303.14K, Condition: Haze
Chennai: 302.23K, Condition: Mist
Bengaluru: 295.25K, Condition: Drizzle
Kolkata: 299.12K, Condition: Light Rain
Hyderabad: 295.38K, Condition: Haze
Database Output (as of 2024-10-23):
Date: 2024-10-23, Avg Temp: 25.90°C, Max Temp: 29.99°C, Min Temp: 22.10°C, Dominant Condition: Haze
Graphical Output: Using matplotlib, the system generates visual representations of daily weather trends and alert conditions.






