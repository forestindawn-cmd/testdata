"""
OpenWeather API를 사용하여 날씨 데이터를 가져오는 모듈
"""
import requests
import json
from datetime import datetime

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0"
    
    def get_coordinates(self, city_name):
        """도시 이름으로 위도, 경도를 가져옵니다."""
        try:
            url = f"{self.geocoding_url}/direct"
            params = {
                'q': city_name,
                'limit': 1,
                'appid': self.api_key
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon'], data[0]['country']
            else:
                return None, None, None
        except Exception as e:
            print(f"좌표 조회 중 오류 발생: {e}")
            return None, None, None
    
    def get_current_weather(self, city_name):
        """현재 날씨 정보를 가져옵니다."""
        try:
            lat, lon, country = self.get_coordinates(city_name)
            if lat is None or lon is None:
                return None
            
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric',  # 섭씨 온도 사용
                'lang': 'kr'        # 한국어 설명
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # 데이터 정리
            weather_data = {
                'city': data['name'],
                'country': country,
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'visibility': data.get('visibility', 0) / 1000,  # km로 변환
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'weather_main': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'weather_icon': data['weather'][0]['icon'],
                'clouds': data['clouds']['all'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                'timezone': data['timezone'],
                'dt': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return weather_data
            
        except Exception as e:
            print(f"현재 날씨 조회 중 오류 발생: {e}")
            return None
    
    def get_5day_forecast(self, city_name):
        """5일 날씨 예보를 가져옵니다."""
        try:
            lat, lon, country = self.get_coordinates(city_name)
            if lat is None or lon is None:
                return None
            
            url = f"{self.base_url}/forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'kr'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            forecast_list = []
            for item in data['list']:
                forecast_item = {
                    'datetime': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M'),
                    'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'),
                    'time': datetime.fromtimestamp(item['dt']).strftime('%H:%M'),
                    'temperature': round(item['main']['temp']),
                    'feels_like': round(item['main']['feels_like']),
                    'temp_min': round(item['main']['temp_min']),
                    'temp_max': round(item['main']['temp_max']),
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'weather_main': item['weather'][0]['main'],
                    'weather_description': item['weather'][0]['description'],
                    'weather_icon': item['weather'][0]['icon'],
                    'clouds': item['clouds']['all'],
                    'wind_speed': item['wind']['speed'],
                    'wind_direction': item['wind'].get('deg', 0),
                    'pop': item.get('pop', 0) * 100  # 강수 확률을 %로 변환
                }
                forecast_list.append(forecast_item)
            
            return forecast_list
            
        except Exception as e:
            print(f"5일 예보 조회 중 오류 발생: {e}")
            return None
    
    def get_weather_icon_url(self, icon_code):
        """날씨 아이콘 URL을 반환합니다."""
        return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"