@echo off
echo 🚀 Streamlit Cloud 배포 준비 중...

REM Git 초기화 (아직 초기화되지 않은 경우)
if not exist ".git" (
    echo 📝 Git 저장소 초기화...
    git init
    git branch -M main
)

REM 모든 파일 추가
echo 📦 파일들을 Git에 추가...
git add .

REM 커밋
echo 💾 변경사항 커밋...
git commit -m "Ready for Streamlit Cloud deployment"

echo.
echo ✅ 배포 준비 완료!
echo.
echo 다음 단계:
echo 1. GitHub에 저장소를 만들고 원격 저장소 연결:
echo    git remote add origin ^<your-github-repo-url^>
echo    git push -u origin main
echo.
echo 2. Streamlit Cloud에서 배포:
echo    - https://share.streamlit.io/ 방문
echo    - GitHub 계정으로 로그인
echo    - 'New app' 클릭
echo    - 저장소 선택 및 app.py 지정
echo    - Secrets에 OPENWEATHER_API_KEY 설정
echo    - Deploy 클릭
echo.
echo 🌤️ 행운을 빕니다!
pause