"""
OpenWeather API를 사용하여 날씨 데이터를 가져오는 모듈
한글 지역명 검색과 구/동 단위 검색을 지원합니다.
"""
import requests
import json
from datetime import datetime, timezone, timedelta
from korean_locations import search_korean_location, get_all_korean_locations

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0"
    
    def get_coordinates(self, city_name):
        """도시 이름으로 위도, 경도를 가져옵니다. 한글 검색을 지원합니다."""
        try:
            # 1. 먼저 한글 지역명 데이터베이스에서 검색
            english_location = search_korean_location(city_name)
            if english_location:
                # 한글 -> 영문 변환된 지역명으로 검색
                search_query = english_location
                print(f"한글 지역 '{city_name}' -> 영문 '{english_location}'로 변환하여 검색")
            else:
                # 영문 그대로 또는 한글 그대로 검색
                search_query = city_name
            
            url = f"{self.geocoding_url}/direct"
            params = {
                'q': search_query,
                'limit': 5,  # 더 많은 결과를 가져와서 정확도 향상
                'appid': self.api_key
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data:
                # 가장 적합한 결과 선택 (첫 번째 결과 우선)
                best_match = data[0]
                
                # 한국 지역인 경우 더 정확한 매칭 시도
                for location in data:
                    if location.get('country') == 'KR':
                        best_match = location
                        break
                
                return best_match['lat'], best_match['lon'], best_match.get('country', 'Unknown')
            else:
                print(f"'{city_name}' 지역을 찾을 수 없습니다.")
                return None, None, None
                
        except Exception as e:
            print(f"좌표 조회 중 오류 발생: {e}")
            return None, None, None
    
    def search_locations(self, query, limit=5):
        """
        지역 검색 기능 - 한글 검색어로 여러 결과를 반환합니다.
        자동완성 기능을 위해 사용됩니다.
        """
        try:
            results = []
            
            # 1. 한국 지역 데이터베이스에서 검색
            all_korean_locations = get_all_korean_locations()
            for korean_name, english_name in all_korean_locations.items():
                if query.lower() in korean_name.lower():
                    results.append({
                        'korean_name': korean_name,
                        'english_name': english_name,
                        'display_name': f"{korean_name} ({english_name})",
                        'type': 'local_db'
                    })
            
            # 2. OpenWeather API에서도 검색 (영문)
            try:
                url = f"{self.geocoding_url}/direct"
                params = {
                    'q': query,
                    'limit': limit,
                    'appid': self.api_key
                }
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                api_data = response.json()
                for location in api_data:
                    location_name = location.get('name', '')
                    state = location.get('state', '')
                    country = location.get('country', '')
                    
                    display_name = location_name
                    if state:
                        display_name += f", {state}"
                    if country:
                        display_name += f", {country}"
                    
                    results.append({
                        'korean_name': location_name,
                        'english_name': location_name,
                        'display_name': display_name,
                        'type': 'api',
                        'lat': location.get('lat'),
                        'lon': location.get('lon'),
                        'country': country
                    })
            except:
                pass  # API 검색 실패해도 로컬 DB 결과는 반환
            
            # 중복 제거 및 정렬
            unique_results = []
            seen_names = set()
            
            for result in results:
                key = result['korean_name'].lower()
                if key not in seen_names:
                    seen_names.add(key)
                    unique_results.append(result)
            
            # 한국 지역 우선, 그 다음 길이순 정렬
            unique_results.sort(key=lambda x: (
                0 if x['type'] == 'local_db' else 1,
                len(x['korean_name'])
            ))
            
            return unique_results[:limit]
            
        except Exception as e:
            print(f"지역 검색 중 오류 발생: {e}")
            return []
    
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
                'sunrise': self._convert_utc_to_local(data['sys']['sunrise'], data['timezone']).strftime('%H:%M'),
                'sunset': self._convert_utc_to_local(data['sys']['sunset'], data['timezone']).strftime('%H:%M'),
                'timezone': data['timezone'],
                'dt': self._convert_utc_to_local(data['dt'], data['timezone']).strftime('%Y-%m-%d %H:%M:%S')
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
            
            # 타임존 정보 가져오기 (도시의 타임존 오프셋)
            timezone_offset = data.get('city', {}).get('timezone', 0)
            
            forecast_list = []
            for item in data['list']:
                # 지역 시간으로 변환
                local_dt = self._convert_utc_to_local(item['dt'], timezone_offset)
                
                forecast_item = {
                    'datetime': local_dt.strftime('%Y-%m-%d %H:%M'),
                    'date': local_dt.strftime('%Y-%m-%d'),
                    'time': local_dt.strftime('%H:%M'),
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
    
    def _convert_utc_to_local(self, utc_timestamp, timezone_offset):
        """
        UTC 타임스탬프를 지역 시간으로 변환합니다.
        
        Args:
            utc_timestamp: UTC 타임스탬프 (초)
            timezone_offset: UTC로부터의 오프셋 (초)
        
        Returns:
            datetime: 지역 시간으로 변환된 datetime 객체
        """
        # UTC 시간으로 datetime 객체 생성
        utc_dt = datetime.fromtimestamp(utc_timestamp, tz=timezone.utc)
        
        # 지역 시간으로 변환
        local_tz = timezone(timedelta(seconds=timezone_offset))
        local_dt = utc_dt.astimezone(local_tz)
        
        return local_dt
    
    def get_current_weather_by_coords(self, lat, lon):
        """
        위도, 경도로 현재 날씨 정보를 가져옵니다.
        현재 위치 기반 날씨 조회에 사용됩니다.
        """
        try:
            url = f"{self.base_url}/weather"
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
            
            # 데이터 정리
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'coordinates': {'lat': lat, 'lon': lon},
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'visibility': data.get('visibility', 0) / 1000,
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'weather_main': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'weather_icon': data['weather'][0]['icon'],
                'clouds': data['clouds']['all'],
                'sunrise': self._convert_utc_to_local(data['sys']['sunrise'], data['timezone']).strftime('%H:%M'),
                'sunset': self._convert_utc_to_local(data['sys']['sunset'], data['timezone']).strftime('%H:%M'),
                'timezone': data['timezone'],
                'dt': self._convert_utc_to_local(data['dt'], data['timezone']).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return weather_data
            
        except Exception as e:
            print(f"좌표 기반 날씨 조회 중 오류 발생: {e}")
            return None
    
    def get_5day_forecast_by_coords(self, lat, lon):
        """
        위도, 경도로 5일 날씨 예보를 가져옵니다.
        현재 위치 기반 예보 조회에 사용됩니다.
        """
        try:
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
            
            # 타임존 정보 가져오기
            timezone_offset = data.get('city', {}).get('timezone', 0)
            
            forecast_list = []
            for item in data['list']:
                # 지역 시간으로 변환
                local_dt = self._convert_utc_to_local(item['dt'], timezone_offset)
                
                forecast_item = {
                    'datetime': local_dt.strftime('%Y-%m-%d %H:%M'),
                    'date': local_dt.strftime('%Y-%m-%d'),
                    'time': local_dt.strftime('%H:%M'),
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
                    'pop': item.get('pop', 0) * 100
                }
                forecast_list.append(forecast_item)
            
            return forecast_list
            
        except Exception as e:
            print(f"좌표 기반 5일 예보 조회 중 오류 발생: {e}")
            return None

    def get_weather_icon_url(self, icon_code):
        """날씨 아이콘 URL을 반환합니다."""
        return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"