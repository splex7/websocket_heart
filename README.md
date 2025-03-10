Trae Cheer - 실시간 인터랙티브 하트 클릭
프로젝트 구조
이 프로젝트는 두 개의 주요 컴포넌트로 구성됩니다:

client/: React 프론트엔드 애플리케이션
server/: WebSocket을 지원하는 Flask 백엔드 서버
배포 가이드
프론트엔드 배포 (Netlify)
코드를 GitHub 저장소에 푸시합니다.
Netlify에 로그인하고 Git에서 새 사이트를 생성합니다.
저장소를 선택합니다.
빌드 설정을 구성합니다.
빌드 명령어: npm run build
배포 디렉터리: dist
기본 디렉터리: client
환경 변수를 추가합니다.
VITE_BACKEND_URL: 백엔드 서버 URL을 설정 (예: https://your-replit-app.replit.app)
백엔드 배포 (Replit)
Replit에 로그인합니다.
새로운 Python Repl을 생성합니다.
server/ 폴더의 코드를 Replit 프로젝트에 업로드합니다.
requirements.txt 파일을 추가하고 필요한 패키지를 포함합니다.
nginx
복사
편집
Flask
Flask-SocketIO
eventlet
main.py 파일을 만들고 Flask 서버를 실행하도록 설정합니다.
Replit에서 "Run" 버튼을 눌러 서버를 실행합니다.
Replit에서 제공하는 공개 URL을 복사하여 Netlify의 VITE_BACKEND_URL 환경 변수에 설정합니다.
중요 설정 사항
CORS 설정

백엔드는 기본적으로 cors_allowed_origins="*"로 설정되어 있습니다.
보안 강화를 위해 배포 시 특정 프론트엔드 도메인만 허용하세요.
python
복사
편집
socketio = SocketIO(app, cors_allowed_origins=["https://your-frontend-domain.netlify.app"])
환경 변수 설정

프론트엔드 (Netlify)
VITE_BACKEND_URL: Replit에서 제공하는 백엔드 URL
백엔드 (Replit)
SECRET_KEY: Flask 보안 키
기타 민감한 데이터는 Replit Secrets 기능을 활용해 설정
SSL/HTTPS 지원

Netlify는 자동으로 SSL/HTTPS를 제공합니다.
Replit의 경우, 무료 플랜에서는 HTTP만 제공되므로 Cloudflare 등의 프록시를 활용해 HTTPS를 적용할 수 있습니다.
모니터링 및 로그 확인

프론트엔드 Netlify 로그 확인
Replit의 콘솔을 통해 실시간 로그 모니터링 가능
웹소켓 및 성능 고려 사항

WebSocket은 지속적인 연결이 필요하므로, Replit에서 서버가 자동 종료되지 않도록 설정해야 합니다.
예상되는 트래픽에 따라 적절한 서버 확장이 필요할 수 있습니다.
문제 해결

WebSocket 연결이 실패하는 경우
CORS 설정 확인
프론트엔드에서 올바른 백엔드 URL 사용 여부 확인
Replit 서버가 실행 중인지 확인
프론트엔드 배포 오류 발생 시 Netlify 로그 확인
백엔드 오류 발생 시 Replit 콘솔 로그 확인
이제 실시간 하트 애니메이션을 즐겨보세요! ❤️
