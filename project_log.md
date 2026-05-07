# 프로젝트 기록 (MNIST 기반 숫자 인식 서비스)

## 1. 프로젝트 개요 및 초안
**아이디어**: MNIST 숫자 데이터 모티브 → 숫자를 그리면 어떤 숫자인지 판별하는 서비스

### 기능1-전: 선행 학습 (모델 및 전처리 설계)
- MNIST 데이터셋을 통해 선행 training 진행.
- 입력 데이터 전처리(Pre-processing)의 한계 극복
  - MNIST 데이터셋은 크기와 위치가 정규화 되어있으므로 숫자가 그려진 영역을 추출하여 중앙으로 정렬하고 MNIST와 같은 비율로 리사이징하는 전처리 파이프라인이 필수
  - 이때 전처리 전 입력데이터가 저장(정답이) 될 가능성이 있으므로 전처리 전 입력데이터를 유지해야함
- MLP 구조 및 하이퍼파라미터 구체화
  - 입력층: 784 노드
  - 은닉층: 2개(512-256 노드) / ReLU
  - 출력층: 10노드(0~9) / Softmax
  - Loss function: Categorical cross-entropy
  - 최적화알고리즘: adam
  - learning rate: 0.001
  - batch size: 64
  - epochs: 16
  - dropout: 0.2

### 기능1-중: 모델 저장 및 서빙 아키텍처
- 모델 저장 포맷 : TensorFlow/Keras
- 서빙 방식 구체화: 프론트엔드에서 그린 이미지를 FastAPI로 전송하면, 서버에 로드된 모델이 추론하여 결과값을 반환

### 기능 1-후: 예외 처리 및 지속적 학습
- 빈 캔버스(숫자 미입력) 처리 아이디어
  - 픽셀 값의 분산이나 총합을 계산하여 일정 임계치(Threshold) 이하이면 모델 추론을 아예 실행하지 않고, "숫자를 먼저 그려주세요"라는 알림(Alert)을 띄우도록 프론트엔드 단에서 예외 처리
- 예측값 오차 및 Overfitting 방지 (피드백 루프 설계)
  - 문제 : 새로운 데이터에만 편향되어 기존 학습 데이터(MNIST)의 특징을 잊어버리는CatastrophicForgetting(파국적 망각) 현상이 발생할 수 있다.
  - 해결 : 새로운 데이터를 바로 학습시키지 않고 데이터베이스에 차곡차곡 모아둔다. 이후 일정 주기(데이터 100개가 모일 때)마다 기존 MNIST 데이터의 일부와 새로 수집된 사용자 데이터를 섞어서(Batch Update) 미세 조정(Fine-tuning) 학습을 진행한다.
- 이상한 그림 처리
  - 사용자가 숫자가 아닌 낙서를 했을 경우를 대비해 , Softmax 출력의 최댓값이 0.6 미만일 경우 “숫자를 추측하기 어렵습니다. 다시 그려주세요.”라고 출력하는 로직 추가

### 기능2: 웹사이트 (UI 및 DB 연동)
- 그리기 도구 구현: HTML5 `<canvas>` 요소를 활용하여 마우스의 좌표 이벤트(`mousedown`, `mousemove`, `mouseup`)를 추적해 선을 렌더링. 브러시 두께와 부드러운 선 처리를 위한 CSS 및 렌더링 설정 필요.
- 데이터베이스 설계: 
  - `id` (Primary Key)
  - `image_data` (이미지 파일 저장 경로)
  - `processed_image` (전처리 이미지 파일 저장 경로)
  - `predicted_label` (모델이 예측한 값)
  - `actual_label` (사용자가 맞다고 컨펌한 값)
  - `created_at` (입력 시간)

### 기능3: 서버 배포
- 환경 격리 및 배포: Docker를 통해 환경을 컨테이너화
- 플랫폼: 개발 후 결정

---

## 2. 기술 스택 요약 (Tech Stack)
- **언어:** Python 3.9+ (백엔드 및 ML), JavaScript (프론트엔드)
- **머신러닝:** TensorFlow/Keras
- **전처리:** OpenCV (`cv2`) (권장), NumPy
- **백엔드:** FastAPI, Uvicorn
- **데이터베이스:** SQLite (개발) -> PostgreSQL/MySQL (배포)
- **ORM:** SQLAlchemy
- **프론트엔드:** HTML5, CSS3, Vanilla JavaScript
- **인프라/배포:** Docker, Docker Compose

---

## 3. 구조적 피드백 및 보완점
- **피드백 1: DB에 이미지 데이터를 저장하는 방식**
  - 서버 내의 특정 폴더(`/images/raw/`, `/images/processed/`)에 이미지 파일을 저장하고, DB에는 파일 경로(Path) 문자열만 저장.
- **피드백 2: 재학습(Fine-tuning) 시점의 서버 멈춤 현상**
  - 재학습 로직은 FastAPI의 `BackgroundTasks` 활용 또는 별도 Python 스크립트로 분리하여 `cron` 작업 등으로 비동기/주기적 실행 처리.
- **피드백 3: 전처리 라이브러리 선택**
  - OpenCV(`cv2`)의 `cv2.findContours` 등을 사용하여 그려진 선의 외곽선을 찾아 자르는 로직 권장.

---

## 4. 개발 워크플로우 (Phase 1 ~ 6)

### Phase 1: 핵심 인공지능 구현 (Jupyter Notebook / Colab)
- [ ] MNIST 데이터셋 로드 및 하이퍼파라미터 적용
- [ ] MLP 모델 구성, 학습 및 성능 확인
- [ ] 학습된 모델 `.h5` 저장 (`mlp_model_v1.h5`)

### Phase 2: 전처리 파이프라인 및 백엔드 구축 (FastAPI)
- [ ] FastAPI 기본 서버 세팅
- [ ] 전처리 함수 구현 (Base64 디코딩 -> Bounding Box 추출 -> 중앙 정렬 -> 28x28 리사이징 -> 1차원 배열)
- [ ] 서버 시작 시 모델 로드
- [ ] 예측 API (`/predict`) 구현 (최댓값 0.6 미만 예외처리 포함)

### Phase 3: 프론트엔드 UI 및 API 연동 (HTML/JS)
- [ ] HTML5 `<canvas>` 드로잉 툴 구현
- [ ] 빈 캔버스 예외 처리
- [ ] 예측 요청 로직 (Base64 변환 후 전송)
- [ ] 결과 및 컨펌 UI ("맞나요? O/X") 구현

### Phase 4: 데이터베이스 연동 및 데이터 수집
- [ ] SQLAlchemy를 이용해 DB 스키마 생성
- [ ] 사용자 피드백 데이터 저장 API (`/feedback`) 구현

### Phase 5: 지속적 학습(Continual Learning) 파이프라인 구축
- [ ] 새 데이터 100개 누적 확인 로직
- [ ] 기존 모델 로드 + 새 데이터 + MNIST 샘플 -> Fine-tuning (백그라운드/비동기)
- [ ] 새 모델 갱신 및 메모리 업데이트

### Phase 6: 도커라이징 및 배포
- [ ] Dockerfile 작성 및 컨테이너화
- [ ] 클라우드 서버 배포

---

## 5. 진행 현황 및 실행 내용 기록
*(여기에 이후 진행되는 프롬프트와 작업 내역, 주요 결정 사항들을 기록합니다.)*

### 2026-05-07 작업 내역
**프롬프트**: "이제 Phase 1을 개발하고 싶은데 내가 해야할 일을 단계적으로 알려줄래? models 파일에 해야할일 텍스트을 작성해줘. 물론 상시로 project_log 파일에 프롬프트 내용도 기록해줘"
**실행 내용**:
- `models/Phase1_TODO.txt` 파일을 생성하여 Phase 1(핵심 인공지능 구현)에서 진행해야 할 세부 단계와 코딩 가이드를 작성함.

