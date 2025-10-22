# 🌤️ 날씨 정보 웹 애플리케이션

OpenWeather API를 사용하여 실시간 날씨 정보와 5일 예보를 제공하는 Streamlit 웹 애플리케이션입니다.

## ✨ 주요 기능

- **실시간 날씨 정보**: 현재 온도, 습도, 기압, 풍속, 가시거리 등
- **5일 날씨 예보**: 3시간 간격의 상세한 날씨 예보
- **시각화**: 온도, 습도, 풍속, 강수확률의 시간별 변화 차트
- **한글 지역 검색**: 🆕 한글로 도시, 구, 동 단위 검색 가능
- **구/동 단위 검색**: 🆕 서울 강남구, 홍대, 명동 등 세부 지역 검색
- **자동완성**: 🆕 입력하는 동안 실시간 검색 제안
- **인기 지역 바로가기**: 주요 도시와 서울 핫스팟 원클릭 선택
- **다국가 지원**: 전 세계 주요 도시 검색 가능
- **반응형 UI**: 모바일과 데스크톱 모두에서 최적화된 사용자 경험

## 🛠️ 기술 스택

- **Python 3.13+**
- **Streamlit**: 웹 애플리케이션 프레임워크
- **Plotly**: 인터랙티브 차트 라이브러리
- **Pandas**: 데이터 처리
- **Requests**: HTTP 요청 처리
- **OpenWeather API**: 날씨 데이터 제공

## 📦 설치 및 실행

### 1. 저장소 클론

```bash
git clone <repository-url>
cd testdata
```

### 2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

```bash
streamlit run app.py
```

웹 브라우저가 자동으로 열리고 `http://localhost:8501`에서 애플리케이션을 확인할 수 있습니다.

## 🔧 설정

### API 키 설정

현재 `config.py` 파일에 OpenWeather API 키가 포함되어 있습니다:

```python
OPENWEATHER_API_KEY = "bed963520292a4fcf7ee4f9110312c6a"
```

### 환경 변수 사용 (권장)

보안을 위해 환경 변수로 API 키를 관리할 수 있습니다:

1. `.env` 파일 생성:
```
OPENWEATHER_API_KEY=bed963520292a4fcf7ee4f9110312c6a
```

2. `app.py`에서 환경 변수 사용:
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
```

## 📁 프로젝트 구조

```
testdata/
├── .streamlit/
│   ├── config.toml     # Streamlit 설정 파일
│   └── secrets.toml    # 로컬 개발용 비밀 키 (Git에서 제외)
├── app.py              # 메인 Streamlit 애플리케이션
├── weather_api.py      # OpenWeather API 연동 모듈
├── korean_locations.py # 🆕 한국 지역 데이터베이스 및 검색 모듈
├── config.py          # 설정 파일
├── requirements.txt   # 필요한 패키지 목록
├── .gitignore         # Git 제외 파일 목록
├── deploy.sh          # Linux/Mac 배포 스크립트
├── deploy.bat         # Windows 배포 스크립트
└── README.md         # 프로젝트 문서
```

## 🎯 주요 파일 설명

### `app.py`
- Streamlit 기반의 메인 웹 애플리케이션
- 사용자 인터페이스 및 시각화 구현
- 날씨 데이터 표시 및 차트 생성

### `weather_api.py`
- OpenWeather API와의 통신을 담당하는 클래스
- 현재 날씨 정보 및 5일 예보 데이터 처리
- 지오코딩을 통한 도시 좌표 변환
- 🆕 한글 지역명 검색 지원
- 🆕 다중 검색 결과 및 자동완성 기능

### `korean_locations.py` 🆕
- 한국 지역 데이터베이스 관리
- 한글 지역명과 영문 지역명 매핑
- 서울, 부산, 인천의 구별 데이터
- 서울 주요 동 지역 데이터  
- 전국 광역시/도 및 주요 시/군 데이터
- 한글 검색 및 자동완성 기능

### `config.py`
- API 키 및 애플리케이션 설정 관리
- 기본 도시 목록 및 UI 설정

## 🌟 사용 방법

1. **지역 검색 방법 선택**:
   - **직접 입력**: 검색창에 한글 또는 영문으로 입력
   - **인기 지역 선택**: 버튼으로 빠른 선택

2. **한글 검색 예시**:
   - 도시: `서울`, `부산`, `대구`, `제주`
   - 구: `강남구`, `서초구`, `해운대구`
   - 동: `역삼동`, `홍대`, `명동`, `잠실동`

3. **영문 검색 예시**:
   - `Seoul`, `Busan`, `Tokyo`, `London`
   - `Gangnam-gu, Seoul`, `Hongdae, Mapo-gu, Seoul`

4. **자동완성 활용**: 입력 중 나타나는 검색 제안을 클릭

5. **실시간 정보 확인**: 현재 날씨와 5일 예보 확인

## 📊 제공되는 정보

### 현재 날씨
- 온도 및 체감온도
- 날씨 상태 및 아이콘
- 습도, 기압, 가시거리
- 풍속 및 구름량
- 일출/일몰 시간

### 5일 예보
- 3시간 간격 상세 예보
- 최고/최저 온도
- 강수 확률
- 시간별 온도, 습도, 풍속 차트

## 🚀 배포

### Streamlit Cloud (추천)

#### 1. GitHub 저장소 준비
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

#### 2. Streamlit Cloud에서 배포
1. [Streamlit Cloud](https://share.streamlit.io/)에 GitHub 계정으로 로그인
2. "New app" 클릭
3. GitHub 저장소 선택
4. Main file path: `app.py`
5. Advanced settings에서 **Secrets** 설정:
   ```toml
   OPENWEATHER_API_KEY = "bed963520292a4fcf7ee4f9110312c6a"
   ```
6. "Deploy!" 클릭

#### 3. 배포 후 확인사항
- 앱이 정상적으로 로드되는지 확인
- API 호출이 정상적으로 작동하는지 테스트
- 모든 차트와 기능이 정상 작동하는지 확인

### 로컬 개발환경에서 Secrets 사용
로컬에서 개발할 때는 `.streamlit/secrets.toml` 파일을 사용:
```toml
OPENWEATHER_API_KEY = "your-api-key-here"
```

### 기타 배포 옵션

#### Heroku
1. `Procfile` 생성:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Heroku CLI로 배포:
```bash
heroku create your-weather-app
heroku config:set OPENWEATHER_API_KEY="bed963520292a4fcf7ee4f9110312c6a"
git push heroku main
```

#### Railway
1. [Railway](https://railway.app/)에 연결
2. GitHub 저장소 연결
3. 환경 변수 `OPENWEATHER_API_KEY` 설정
4. 자동 배포

## 🤝 기여하기

1. Fork 프로젝트
2. Feature 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 Push (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해주세요.

## 🙏 감사의 말

- [OpenWeather](https://openweathermap.org/) - 날씨 데이터 API 제공
- [Streamlit](https://streamlit.io/) - 웹 애플리케이션 프레임워크
- [Plotly](https://plotly.com/) - 인터랙티브 차트 라이브러리