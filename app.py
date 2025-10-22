"""
Streamlit을 사용한 날씨 웹 애플리케이션
OpenWeather API를 활용하여 현재 날씨와 5일 예보를 제공합니다.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import os
from weather_api import WeatherAPI

# 페이지 설정
st.set_page_config(
    page_title="날씨 정보 앱",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API 키 설정 (환경변수 또는 Streamlit secrets 사용)
API_KEY = st.secrets.get("OPENWEATHER_API_KEY", os.getenv("OPENWEATHER_API_KEY", "bed963520292a4fcf7ee4f9110312c6a"))

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .weather-card {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .forecast-card {
        background: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 메인 타이틀
st.markdown('<h1 class="main-header">🌤️ 실시간 날씨 정보</h1>', unsafe_allow_html=True)

# 사이드바
st.sidebar.header("🔍 도시 검색")
city_input = st.sidebar.text_input("도시 이름을 입력하세요:", value="Seoul", placeholder="예: Seoul, Tokyo, London")

# 인기 도시 버튼
st.sidebar.subheader("🏙️ 인기 도시")
popular_cities = ["Seoul", "Tokyo", "London", "New York", "Paris", "Sydney"]
selected_city = None

cols = st.sidebar.columns(2)
for i, city in enumerate(popular_cities):
    if cols[i % 2].button(city, key=f"city_{city}"):
        selected_city = city

if selected_city:
    city_input = selected_city

# WeatherAPI 인스턴스 생성
weather_api = WeatherAPI(API_KEY)

# 메인 앱 로직
if city_input:
    with st.spinner(f"{city_input}의 날씨 정보를 가져오는 중..."):
        # 현재 날씨 정보 가져오기
        current_weather = weather_api.get_current_weather(city_input)
        
        if current_weather:
            # 현재 날씨 표시
            st.success(f"✅ {current_weather['city']}, {current_weather['country']}의 날씨 정보를 성공적으로 가져왔습니다!")
            
            # 현재 날씨 카드
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="weather-card">
                    <h2>현재 날씨</h2>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 20px;">
                        <img src="{weather_api.get_weather_icon_url(current_weather['weather_icon'])}" 
                             style="width: 100px; height: 100px;">
                        <div>
                            <h1 style="margin: 0; font-size: 4rem;">{current_weather['temperature']}°C</h1>
                            <p style="margin: 0; font-size: 1.2rem;">{current_weather['weather_description']}</p>
                            <p style="margin: 0; opacity: 0.8;">체감온도: {current_weather['feels_like']}°C</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("습도", f"{current_weather['humidity']}%", delta=None)
                st.metric("기압", f"{current_weather['pressure']} hPa", delta=None)
                st.metric("가시거리", f"{current_weather['visibility']} km", delta=None)
            
            with col3:
                st.metric("풍속", f"{current_weather['wind_speed']} m/s", delta=None)
                st.metric("구름", f"{current_weather['clouds']}%", delta=None)
                st.metric("일출", current_weather['sunrise'], delta=None)
                st.metric("일몰", current_weather['sunset'], delta=None)
            
            # 5일 예보 가져오기
            st.subheader("📅 5일 날씨 예보")
            forecast_data = weather_api.get_5day_forecast(city_input)
            
            if forecast_data:
                # 데이터프레임 생성
                df = pd.DataFrame(forecast_data)
                df['datetime'] = pd.to_datetime(df['datetime'])
                
                # 일별 데이터 그룹화 (최고/최저 온도)
                daily_data = df.groupby('date').agg({
                    'temp_max': 'max',
                    'temp_min': 'min',
                    'humidity': 'mean',
                    'weather_description': 'first',
                    'weather_icon': 'first',
                    'pop': 'max'
                }).reset_index()
                
                # 온도 차트
                col1, col2 = st.columns(2)
                
                with col1:
                    # 시간별 온도 변화 차트
                    fig_temp = px.line(df, x='datetime', y='temperature', 
                                     title='시간별 온도 변화',
                                     labels={'temperature': '온도 (°C)', 'datetime': '시간'})
                    fig_temp.update_layout(height=400)
                    st.plotly_chart(fig_temp, use_container_width=True, config={'displayModeBar': False})
                
                with col2:
                    # 습도 차트
                    fig_humidity = px.bar(df, x='time', y='humidity',
                                        title='시간별 습도',
                                        labels={'humidity': '습도 (%)', 'time': '시간'})
                    fig_humidity.update_layout(height=400)
                    st.plotly_chart(fig_humidity, use_container_width=True, config={'displayModeBar': False})
                
                # 일별 예보 카드
                st.subheader("📊 일별 예보")
                cols = st.columns(5)
                
                for i, (_, day) in enumerate(daily_data.iterrows()):
                    if i < 5:  # 5일간만 표시
                        with cols[i]:
                            date_obj = datetime.strptime(day['date'], '%Y-%m-%d')
                            day_name = date_obj.strftime('%m/%d\n%a')
                            
                            st.markdown(f"""
                            <div class="forecast-card">
                                <h4>{day_name}</h4>
                                <img src="{weather_api.get_weather_icon_url(day['weather_icon'])}" 
                                     style="width: 60px; height: 60px;">
                                <p style="margin: 5px 0; font-weight: bold;">
                                    {int(day['temp_max'])}° / {int(day['temp_min'])}°
                                </p>
                                <p style="margin: 0; font-size: 0.8rem; color: #666;">
                                    {day['weather_description']}
                                </p>
                                <p style="margin: 0; font-size: 0.8rem; color: #1f77b4;">
                                    강수: {int(day['pop'])}%
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                
                # 상세 예보 테이블
                with st.expander("📋 상세 예보 보기"):
                    # 표시할 컬럼 선택
                    display_df = df[['datetime', 'temperature', 'feels_like', 'humidity', 
                                   'pressure', 'weather_description', 'wind_speed', 'pop']].copy()
                    display_df.columns = ['날짜/시간', '온도(°C)', '체감온도(°C)', '습도(%)', 
                                        '기압(hPa)', '날씨', '풍속(m/s)', '강수확률(%)']
                    st.dataframe(display_df, use_container_width=True)
                
                # 풍속과 풍향 정보
                st.subheader("💨 바람 정보")
                col1, col2 = st.columns(2)
                
                with col1:
                    # 풍속 차트
                    fig_wind = px.line(df, x='datetime', y='wind_speed',
                                     title='시간별 풍속 변화',
                                     labels={'wind_speed': '풍속 (m/s)', 'datetime': '시간'})
                    st.plotly_chart(fig_wind, use_container_width=True, config={'displayModeBar': False})
                
                with col2:
                    # 강수 확률 차트
                    fig_pop = px.bar(df, x='time', y='pop',
                                   title='시간별 강수 확률',
                                   labels={'pop': '강수 확률 (%)', 'time': '시간'})
                    st.plotly_chart(fig_pop, use_container_width=True, config={'displayModeBar': False})
            
            else:
                st.error("5일 예보 데이터를 가져올 수 없습니다.")
        
        else:
            st.error(f"'{city_input}' 도시의 날씨 정보를 찾을 수 없습니다. 도시 이름을 확인해주세요.")

else:
    st.info("👈 사이드바에서 도시 이름을 입력하거나 인기 도시를 선택해주세요.")
    
    # 기본 정보 표시
    st.markdown("""
    ### 🌟 기능 소개
    
    이 앱은 OpenWeather API를 사용하여 실시간 날씨 정보를 제공합니다:
    
    - **현재 날씨**: 온도, 습도, 기압, 풍속, 가시거리 등
    - **5일 예보**: 시간별, 일별 상세 날씨 예보
    - **시각화**: 온도, 습도, 풍속, 강수확률 차트
    - **다국가 지원**: 전 세계 주요 도시 검색 가능
    
    ### 🚀 사용 방법
    1. 사이드바에서 도시 이름을 입력하세요
    2. 또는 인기 도시 버튼을 클릭하세요
    3. 실시간 날씨 정보와 예보를 확인하세요
    """)

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; padding: 1rem;'>
        🌤️ 날씨 정보 앱 | OpenWeather API 제공 | Made with Streamlit
    </div>
    """, 
    unsafe_allow_html=True
)