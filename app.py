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
from korean_locations import get_popular_korean_locations
from location_service import render_location_component, parse_location_data

# 페이지 설정
st.set_page_config(
    page_title="날씨 정보 앱",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API 키 설정 (환경변수 또는 Streamlit secrets 사용)
API_KEY = st.secrets.get("OPENWEATHER_API_KEY", os.getenv("OPENWEATHER_API_KEY", "bed963520292a4fcf7ee4f9110312c6a"))

# WeatherAPI 인스턴스 생성
weather_api = WeatherAPI(API_KEY)

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
st.sidebar.header("🔍 지역 검색")

# 검색 방법 선택
search_method = st.sidebar.radio(
    "검색 방법을 선택하세요:",
    ["직접 입력", "인기 지역 선택", "📍 현재 위치"]
)

if search_method == "직접 입력":
    city_input = st.sidebar.text_input(
        "지역명을 입력하세요:", 
        value="서울", 
        placeholder="예: 서울, 강남구, 홍대, Busan, Tokyo",
        help="한글 또는 영문으로 입력하세요. 구/동 단위 검색도 가능합니다."
    )
    
    # 실시간 검색 제안 (입력이 있을 때만)
    if city_input and len(city_input) > 1:
        with st.sidebar.expander("💡 검색 제안", expanded=False):
            search_results = weather_api.search_locations(city_input, limit=5)
            
            if search_results:
                st.write("다음 지역들을 찾았습니다:")
                for i, result in enumerate(search_results):
                    if st.button(
                        f"📍 {result['display_name']}", 
                        key=f"suggestion_{i}",
                        help=f"타입: {result['type']}"
                    ):
                        city_input = result['korean_name']
                        st.rerun()
            else:
                st.write("검색 결과가 없습니다.")

elif search_method == "인기 지역 선택":
    # 인기 지역 선택
    popular_locations = get_popular_korean_locations()
    
    st.sidebar.subheader("🏙️ 주요 도시")
    major_cities = popular_locations[:6]
    cols = st.sidebar.columns(2)
    selected_city = None
    
    for i, city in enumerate(major_cities):
        if cols[i % 2].button(city, key=f"major_city_{city}"):
            selected_city = city
    
    st.sidebar.subheader("🏘️ 서울 주요 구역")
    seoul_areas = ["강남구", "홍대", "명동", "잠실동", "압구정동", "이태원"]
    cols = st.sidebar.columns(2)
    
    for i, area in enumerate(seoul_areas):
        if cols[i % 2].button(area, key=f"seoul_area_{area}"):
            selected_city = area
    
    st.sidebar.subheader("🌊 기타 인기 지역")
    other_areas = ["해운대구", "제주", "춘천", "강릉", "부산", "대구"]
    cols = st.sidebar.columns(2)
    
    for i, area in enumerate(other_areas):
        if cols[i % 2].button(area, key=f"other_area_{area}"):
            selected_city = area
    
    city_input = selected_city if selected_city else "서울"

elif search_method == "📍 현재 위치":
    st.sidebar.subheader("🌍 현재 위치 날씨")
    
    # 위치 정보 확인
    lat, lon = parse_location_data()
    
    if lat is not None and lon is not None:
        st.sidebar.success(f"📍 위치 확인: {lat:.4f}, {lon:.4f}")
        city_input = "current_location"
        
        # 세션 스테이트에 좌표 저장
        st.session_state.current_lat = lat
        st.session_state.current_lon = lon
    else:
        st.sidebar.info("위치 정보를 가져오려면 아래 버튼을 클릭하세요.")
        
        # 위치 가져오기 컴포넌트 렌더링
        render_location_component()
        
        # URL 파라미터로 위치 정보가 전달된 경우 처리
        query_params = st.query_params
        if "lat" in query_params and "lon" in query_params:
            try:
                lat = float(query_params["lat"])
                lon = float(query_params["lon"])
                st.session_state.current_lat = lat
                st.session_state.current_lon = lon
                st.sidebar.success(f"📍 위치 업데이트: {lat:.4f}, {lon:.4f}")
                st.rerun()
            except:
                st.sidebar.error("위치 정보 파싱 오류")
        
        # 기본값으로 서울 설정
        city_input = "서울"

# 검색 팁 표시
with st.sidebar.expander("💭 검색 팁", expanded=False):
    st.markdown("""
    **한글 검색 예시:**
    - 도시: 서울, 부산, 대구
    - 구: 강남구, 서초구, 해운대구  
    - 동: 역삼동, 홍대, 명동
    
    **영문 검색 예시:**
    - Seoul, Busan, Tokyo
    - Gangnam-gu, Seoul
    - Hongdae, Mapo-gu, Seoul
    
    **검색 범위:**
    - 전국 광역시/도
    - 서울 전체 구/동
    - 부산, 인천 주요 구역
    - 전국 주요 시/군
    
    **📍 현재 위치 사용법:**
    1. "📍 현재 위치" 선택
    2. "현재 위치 날씨 보기" 버튼 클릭
    3. 브라우저에서 위치 접근 허용
    4. 자동으로 현재 위치 날씨 표시
    
    ⚠️ 위치 기능 사용시 주의사항:
    - HTTPS 연결에서만 정상 작동
    - 브라우저에서 위치 접근 허용 필요
    - 정확도는 기기 및 환경에 따라 다름
    """)

# 메인 앱 로직
if city_input:
    # 현재 위치 날씨인지 확인
    if city_input == "current_location" and hasattr(st.session_state, 'current_lat'):
        lat = st.session_state.current_lat
        lon = st.session_state.current_lon
        
        with st.spinner(f"현재 위치 ({lat:.4f}, {lon:.4f})의 날씨 정보를 가져오는 중..."):
            # 좌표 기반 현재 날씨 정보 가져오기
            current_weather = weather_api.get_current_weather_by_coords(lat, lon)
    else:
        with st.spinner(f"{city_input}의 날씨 정보를 가져오는 중..."):
            # 일반 도시명 기반 현재 날씨 정보 가져오기
            current_weather = weather_api.get_current_weather(city_input)
        
        if current_weather:
            # 현재 날씨 표시
            location_info = f"{current_weather['city']}, {current_weather['country']}"
            
            # 현재 위치인 경우 좌표 정보도 표시
            if city_input == "current_location" and 'coordinates' in current_weather:
                coords = current_weather['coordinates']
                location_info += f" (📍 {coords['lat']:.4f}, {coords['lon']:.4f})"
            
            st.success(f"✅ {location_info}의 날씨 정보를 성공적으로 가져왔습니다!")
            
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
            
            # 현재 위치인지 확인하여 적절한 API 호출
            if city_input == "current_location" and hasattr(st.session_state, 'current_lat'):
                forecast_data = weather_api.get_5day_forecast_by_coords(
                    st.session_state.current_lat, 
                    st.session_state.current_lon
                )
            else:
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