"""
위치 기반 서비스 모듈
브라우저 Geolocation API를 사용하여 사용자의 현재 위치를 가져옵니다.
"""

import streamlit as st
import streamlit.components.v1 as components

def get_geolocation_js():
    """
    브라우저의 Geolocation API를 사용하는 JavaScript 코드를 반환합니다.
    """
    return """
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            document.getElementById("location-status").innerHTML = "위치 정보를 가져오는 중...";
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    const accuracy = position.coords.accuracy;
                    
                    // Streamlit에 위치 정보 전달
                    const locationData = {
                        latitude: lat,
                        longitude: lon,
                        accuracy: accuracy,
                        timestamp: new Date().toISOString()
                    };
                    
                    // 페이지에 위치 정보 표시
                    document.getElementById("location-status").innerHTML = 
                        `✅ 위치 정보 획득 완료!<br>
                         위도: ${lat.toFixed(6)}<br>
                         경도: ${lon.toFixed(6)}<br>
                         정확도: ${accuracy.toFixed(0)}m`;
                    
                    // Streamlit session state에 저장
                    parent.postMessage({
                        type: 'streamlit:locationUpdate',
                        data: locationData
                    }, '*');
                    
                    // 새로고침하여 Streamlit이 위치 정보를 처리하도록 함
                    setTimeout(() => {
                        parent.postMessage({
                            type: 'streamlit:triggerRerun'
                        }, '*');
                    }, 1000);
                },
                function(error) {
                    let errorMsg = "";
                    switch(error.code) {
                        case error.PERMISSION_DENIED:
                            errorMsg = "❌ 위치 접근이 거부되었습니다. 브라우저 설정을 확인해주세요.";
                            break;
                        case error.POSITION_UNAVAILABLE:
                            errorMsg = "❌ 위치 정보를 사용할 수 없습니다.";
                            break;
                        case error.TIMEOUT:
                            errorMsg = "❌ 위치 정보 요청이 시간 초과되었습니다.";
                            break;
                        default:
                            errorMsg = "❌ 알 수 없는 오류가 발생했습니다.";
                            break;
                    }
                    document.getElementById("location-status").innerHTML = errorMsg;
                }
            );
        } else {
            document.getElementById("location-status").innerHTML = 
                "❌ 이 브라우저는 위치 서비스를 지원하지 않습니다.";
        }
    }
    
    // 메시지 수신 이벤트 리스너
    window.addEventListener('message', function(event) {
        if (event.data.type === 'streamlit:locationUpdate') {
            // 세션 스토리지에 위치 정보 저장
            localStorage.setItem('weatherapp_location', JSON.stringify(event.data.data));
        }
    });
    
    // 페이지 로드시 저장된 위치 정보 확인
    window.onload = function() {
        const savedLocation = localStorage.getItem('weatherapp_location');
        if (savedLocation) {
            const locationData = JSON.parse(savedLocation);
            const timeDiff = new Date() - new Date(locationData.timestamp);
            
            // 10분 이내의 데이터면 표시
            if (timeDiff < 10 * 60 * 1000) {
                document.getElementById("location-status").innerHTML = 
                    `💾 저장된 위치 (${Math.round(timeDiff/60000)}분 전):<br>
                     위도: ${locationData.latitude.toFixed(6)}<br>
                     경도: ${locationData.longitude.toFixed(6)}`;
            }
        }
    };
    </script>
    
    <div style="padding: 20px; border: 2px dashed #1f77b4; border-radius: 10px; text-align: center; background: #f8f9fa;">
        <h4>📍 현재 위치 확인</h4>
        <p>버튼을 클릭하여 현재 위치의 날씨를 확인하세요.</p>
        <button onclick="getLocation()" 
                style="background: #1f77b4; color: white; border: none; padding: 10px 20px; 
                       border-radius: 5px; cursor: pointer; font-size: 16px;">
            📍 현재 위치 날씨 보기
        </button>
        <div id="location-status" style="margin-top: 15px; font-weight: bold;"></div>
        <p style="font-size: 12px; color: #666; margin-top: 10px;">
            ⚠️ 위치 접근 권한이 필요합니다. 브라우저에서 허용을 클릭해주세요.
        </p>
    </div>
    """

def get_location_from_storage():
    """
    로컬 스토리지에서 위치 정보를 가져오는 JavaScript 코드
    """
    js_code = """
    <script>
    function getStoredLocation() {
        const savedLocation = localStorage.getItem('weatherapp_location');
        if (savedLocation) {
            const locationData = JSON.parse(savedLocation);
            const timeDiff = new Date() - new Date(locationData.timestamp);
            
            // 10분 이내의 데이터만 유효
            if (timeDiff < 10 * 60 * 1000) {
                // Streamlit에 위치 정보 전달
                parent.postMessage({
                    type: 'streamlit:setLocation',
                    data: locationData
                }, '*');
                return true;
            }
        }
        return false;
    }
    
    // 페이지 로드시 실행
    getStoredLocation();
    </script>
    """
    return js_code

def render_location_component():
    """
    위치 정보 가져오기 컴포넌트를 렌더링합니다.
    """
    # JavaScript 컴포넌트 렌더링
    components.html(get_geolocation_js(), height=200)

def check_stored_location():
    """
    저장된 위치 정보가 있는지 확인합니다.
    """
    # 간단한 확인용 JavaScript
    components.html(get_location_from_storage(), height=0)

def parse_location_data():
    """
    브라우저에서 받은 위치 데이터를 파싱합니다.
    실제 구현에서는 query_params나 session_state를 사용할 수 있습니다.
    """
    # Streamlit의 query_params를 통해 위치 정보를 받을 수 있습니다
    query_params = st.query_params
    
    if "lat" in query_params and "lon" in query_params:
        try:
            lat = float(query_params["lat"])
            lon = float(query_params["lon"])
            return lat, lon
        except:
            return None, None
    
    return None, None