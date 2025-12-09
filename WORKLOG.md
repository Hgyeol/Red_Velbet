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

### Phase 3: 지갑 도메인 구현

- **브랜치:** `feat/phase3-wallet-domain`
- **작업 내용:** Phase 3 - 지갑 도메인 구현
- **변경 사항:**
  - **도메인 계층:**
    - `src/domain/wallet/entity.py`: Wallet 엔티티 정의 (잔액 입출금 로직 포함)
    - `src/domain/wallet/repository.py`: Wallet Repository 인터페이스 정의
    - `src/domain/wallet/service.py`: Wallet 서비스 정의 (잔액 조회, 입금, 출금)
  - **인프라 계층:**
    - `src/infrastructure/database/models.py`: Wallet 데이터베이스 모델 추가
    - `src/infrastructure/database/repositories/wallet_repository.py`: Wallet Repository 구현
  - **애플리케이션 계층:**
    - `src/application/wallet/dto.py`: Wallet 관련 DTO 정의 (잔액, 입금/출금 요청, 거래 내역)
    - `src/application/wallet/use_cases.py`: Wallet Use Case 정의 (잔액 조회, 입금, 출금)
  - **프레젠테이션 계층:**
    - `src/presentation/schemas/wallet.py`: Wallet 관련 Pydantic 스키마 정의
    - `src/presentation/api/v1/wallet.py`: Wallet API 엔드포인트 구현 (잔액 조회, 입금, 출금)
    - `src/presentation/api/dependencies.py`: Wallet Repository, Wallet Service, Wallet Use Case 의존성 주입 추가
  - **기타:**
    - `src/main.py`: Wallet API 라우터 등록
- **특이 사항:**
  - DDD 아키텍처에 따라 지갑 도메인 구현 완료
  - 사용자 지갑 관리의 핵심 기능(조회, 입금, 출금) 구현
  - 추후 거래 내역 및 배팅 연동 기능 추가 예정

### Phase 4: 리그 도메인 구현

- **브랜치:** `feat/phase4-core-apis`
- **작업 내용:** Phase 4 - 리그 도메인 구현
- **변경 사항:**
  - **도메인 계층:**
    - `src/domain/league/entity.py`: League 엔티티 정의
    - `src/domain/league/repository.py`: League Repository 인터페이스 정의
  - **인프라 계층:**
    - `src/infrastructure/database/models.py`: League, Game, BettingOption, Favorite, Bet, BetSlip, Transaction 데이터베이스 모델 추가 및 관련 Enum 정의
    - `src/infrastructure/database/repositories/league_repository.py`: League Repository 구현
  - **애플리케이션 계층:**
    - `src/application/league/dto.py`: League 관련 DTO 정의
    - `src/application/league/use_cases.py`: League Use Case 정의 (생성, 조회, 수정, 삭제)
  - **프레젠테이션 계층:**
    - `src/presentation/schemas/league.py`: League 관련 Pydantic 스키마 정의
    - `src/presentation/api/v1/leagues.py`: League API 엔드포인트 구현 (CRUD)
    - `src/presentation/api/dependencies.py`: League Repository, League Use Case 의존성 주입 추가
  - **기타:**
    - `src/main.py`: League API 라우터 등록
- **특이 사항:**
  - DDD 아키텍처에 따라 리그 도메인 구현 완료
  - 리그 관리의 핵심 기능(생성, 조회, 수정, 삭제) 구현 완료

### Phase 4.5: 게임 도메인 구현

- **브랜치:** `feat/phase4-core-apis`
- **작업 내용:** Phase 4.5 - 게임 도메인 구현
- **변경 사항:**
  - **도메인 계층:**
    - `src/domain/game/enums.py`: Game 관련 Enum 정의 (SportTypeEnum, GameStatusEnum)
    - `src/domain/game/entity.py`: Game 엔티티 정의 및 비즈니스 로직
    - `src/domain/game/repository.py`: Game Repository 인터페이스 정의
  - **인프라 계층:**
    - `src/infrastructure/database/repositories/game_repository.py`: Game Repository 구현
  - **애플리케이션 계층:**
    - `src/application/game/dto.py`: Game 관련 DTO 정의
    - `src/application/game/use_cases.py`: Game Use Case 정의 (생성, 조회, 수정, 스코어 설정, 삭제)
  - **프레젠테이션 계층:**
    - `src/presentation/schemas/game.py`: Game 관련 Pydantic 스키마 정의
    - `src/presentation/api/v1/games.py`: Game API 엔드포인트 구현 (CRUD 및 스코어 설정)
    - `src/presentation/api/dependencies.py`: Game Repository, Game Use Case 의존성 주입 추가
  - **기타:**
    - `src/main.py`: Game API 라우터 등록
- **특이 사항:**
  - DDD 아키텍처에 따라 게임 도메인 구현 완료
  - 게임 관리의 핵심 기능(CRUD, 스코어 설정) 구현
