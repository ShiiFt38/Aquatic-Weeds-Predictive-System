import requests
from datetime import datetime, timedelta
from typing import Dict, Any


class WeatherHandler:
    def __init__(self, db):
        self.db = db
        # Hartbeespoortdam coordinates
        self.latitude = -25.7447
        self.longitude = 27.8521
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_weather_data(self, date_str: str) -> Dict[str, Any]:
        try:
            # Validate and parse date
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
            current_date = datetime.now()

            # Check if date is within reasonable range (7 days past to 7 days future)
            if target_date < current_date - timedelta(days=7) or target_date > current_date + timedelta(days=7):
                print(f"Warning: Date {date_str} might be outside the available range. Using historical API endpoint.")
                return self.get_historical_weather_data(date_str)

            # Define parameters for the API request
            params = {
                'latitude': self.latitude,
                'longitude': self.longitude,
                'daily': [
                    'temperature_2m_max',
                    'temperature_2m_min',
                    'precipitation_sum',
                    'rain_sum',
                    'windspeed_10m_max'
                ],
                'timezone': 'Africa/Johannesburg',
                'start_date': date_str,
                'end_date': date_str
            }

            # Make the API request
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            # Print raw response for debugging
            data = response.json()
            print("\nAPI Response:", data)  # Debug print

            if 'daily' not in data:
                raise ValueError("No daily weather data available")

            # Extract the daily weather data
            weather_info = {
                'date': data['daily']['time'][0],
                'max_temp': data['daily']['temperature_2m_max'][0],
                'min_temp': data['daily']['temperature_2m_min'][0],
                'precipitation': data['daily']['precipitation_sum'][0],
                'rain': data['daily']['rain_sum'][0],
                'max_windspeed': data['daily']['windspeed_10m_max'][0]
            }

            return weather_info

        except ValueError as e:
            print(f"Error: Invalid date format. Please use YYYY-MM-DD format. Details: {str(e)}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to fetch weather data. Details: {str(e)}")
            return None
        except Exception as e:
            print(f"Error: An unexpected error occurred. Details: {str(e)}")
            return None

    def get_historical_weather_data(self, date_str: str) -> Dict[str, Any]:
        """
        Get historical weather data using the archive API endpoint.
        """
        try:
            historical_url = "https://archive-api.open-meteo.com/v1/archive"
            params = {
                'latitude': self.latitude,
                'longitude': self.longitude,
                'daily': [
                    'temperature_2m_max',
                    'temperature_2m_min',
                    'precipitation_sum',
                    'rain_sum',
                    'windspeed_10m_max'
                ],
                'timezone': 'Africa/Johannesburg',
                'start_date': date_str,
                'end_date': date_str
            }

            response = requests.get(historical_url, params=params)
            response.raise_for_status()

            # Print raw response for debugging
            data = response.json()
            print("\nHistorical API Response:", data)  # Debug print

            if 'daily' not in data:
                raise ValueError("No daily weather data available")

            weather_info = {
                'date': data['daily']['time'][0],
                'max_temp': data['daily']['temperature_2m_max'][0],
                'min_temp': data['daily']['temperature_2m_min'][0],
                'precipitation': data['daily']['precipitation_sum'][0],
                'rain': data['daily']['rain_sum'][0],
                'max_windspeed': data['daily']['windspeed_10m_max'][0]
            }

            if weather_info:
                self.db.store_weather_data(weather_info)

            return weather_info

        except Exception as e:
            print(f"Error fetching historical data: {str(e)}")
            return None

    def print_weather_data(self, weather_info: Dict[str, Any]) -> None:
        if weather_info:
            print("\nWeather Report for Hartbeespoortdam, Pretoria")
            print("=" * 45)
            print(f"Date: {weather_info['date']}")
            print(f"Maximum Temperature: {weather_info['max_temp']}°C")
            print(f"Minimum Temperature: {weather_info['min_temp']}°C")
            print(f"Total Precipitation: {weather_info['precipitation']} mm")
            print(f"Total Rainfall: {weather_info['rain']} mm")
            print(f"Maximum Wind Speed: {weather_info['max_windspeed']} km/h")
            print("=" * 45)