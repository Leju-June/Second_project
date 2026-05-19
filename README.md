# Second_project
2학년 1,2학기 개인 개발 프로젝트

project_log.md : 전체 개발 계획 및 회고 기록
이 프로젝트는 AI를 통해 계획을 수립하고 직접 개발한 후, AI의 피드백을 통해 개선하는 과정으로 진행되었습니다.
이를 통해 웹 서비스의 전체적인 개발 과정과 배포 방식을 이해하는 것을 목표로 하였습니다.
위 포부를 최대한 지키기 위해 코드를 대신 작성하는 프롬프트는 작성하지 않았습니다. (project_log 참고)

# requirements.txt
이 프로젝트 실행에 필요한 패키지를 모은 파일입니다.
pip install -r requirements.txt
를 입력하면 패키지를 설치할 수 있습니다.

# 프로젝트 실행 방법
1. 가상환경 설정
pip -m venv .venv
. .venv/Scripts/activate
2. 패키지 설치
pip install -r requirements.txt
3. FastAPI 서버 실행
uvicorn backend.main:app --reload