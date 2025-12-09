# 작업일지

이 파일은 프로젝트의 모든 작업 내역을 기록합니다.

## 2025-12-09

### Phase 1: 기본 인프라 구축

- **브랜치:** `feat/phase1-infrastructure`
- **작업 내용:** Phase 1 - 기본 인프라 구축
- **변경 사항:**
  - DDD 디렉토리 구조 생성 (domain, application, infrastructure, presentation 계층)
  - `Dockerfile`: FastAPI 애플리케이션 컨테이너 이미지 설정
  - `docker-compose.yml`: MySQL, Redis, FastAPI 컨테이너 구성
  - `.env`: 환경 변수 설정 (데이터베이스, Redis, JWT, 앱 설정)
  - `.gitignore`: Git 제외 파일 설정
  - `requirements.txt`: Python 의존성 패키지 목록
  - `src/main.py`: FastAPI 기본 애플리케이션 (헬스 체크 엔드포인트)
  - `src/config.py`: 애플리케이션 설정 관리 (Pydantic Settings)
  - `scripts/init.sql`: MySQL 초기화 스크립트
- **특이 사항:** Docker Compose 환경으로 로컬 개발 환경 구축 완료

### Phase 2: 인증 시스템 구현

- **브랜치:** `feat/phase2-auth-system`
- **작업 내용:** Phase 2 - 인증 및 사용자 관리 시스템 구현
- **변경 사항:**
  - **도메인 계층:**
    - `src/domain/user/entity.py`: User 엔티티 및 비즈니스 로직
    - `src/domain/user/repository.py`: User Repository 인터페이스
    - `src/domain/common/value_objects.py`: Email, Username, Password Value Objects
    - `src/domain/common/exceptions.py`: 도메인 예외 정의
  - **인프라 계층:**
    - `src/infrastructure/auth/password_hasher.py`: bcrypt 비밀번호 해싱
    - `src/infrastructure/auth/jwt_handler.py`: JWT 토큰 생성/검증
    - `src/infrastructure/auth/token_repository.py`: Refresh Token Redis 저장소
    - `src/infrastructure/cache/redis_client.py`: Redis 클라이언트
    - `src/infrastructure/database/connection.py`: SQLAlchemy 비동기 연결
    - `src/infrastructure/database/models.py`: User 데이터베이스 모델
    - `src/infrastructure/database/repositories/user_repository.py`: User Repository 구현
  - **애플리케이션 계층:**
    - `src/application/user/dto.py`: User 및 Auth DTO
    - `src/application/user/use_cases.py`: 회원가입, 로그인, 토큰갱신, 로그아웃, 비밀번호변경 등
  - **프레젠테이션 계층:**
    - `src/presentation/schemas/auth.py`: 인증 관련 Pydantic 스키마
    - `src/presentation/schemas/user.py`: 사용자 관련 Pydantic 스키마
    - `src/presentation/api/dependencies.py`: FastAPI 의존성 주입
    - `src/presentation/api/v1/auth.py`: 인증 API 엔드포인트
    - `src/presentation/api/v1/users.py`: 사용자 API 엔드포인트
  - **기타:**
    - `src/main.py`: API 라우터 등록 및 DB/Redis 연결 초기화
    - `requirements.txt`: aiomysql 추가
- **특이 사항:**
  - 완전한 DDD 아키텍처로 인증 시스템 구현
  - bcrypt 비밀번호 해싱, JWT 토큰 기반 인증
  - Refresh Token을 Redis에 저장
