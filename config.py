"""
설정 파일
API 키와 기타 설정값을 관리합니다.
"""

# OpenWeather API 설정
OPENWEATHER_API_KEY = "bed963520292a4fcf7ee4f9110312c6a"
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"
OPENWEATHER_GEOCODING_URL = "http://api.openweathermap.org/geo/1.0"

# Streamlit 앱 설정
APP_TITLE = "날씨 정보 앱"
APP_ICON = "🌤️"

# 기본 도시 목록
DEFAULT_CITIES = [
    "Seoul", "Tokyo", "London", "New York", 
    "Paris", "Sydney", "Beijing", "Singapore"
]

# 언어 설정
WEATHER_LANGUAGE = "kr"  # 한국어
TEMPERATURE_UNIT = "metric"  # 섭씨 온도

# UI 설정
CHART_HEIGHT = 400
FORECAST_DAYS = 5