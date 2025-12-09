# 배팅 사이트 백엔드 개발 명세서

## 1. 프로젝트 개요

### 1.1 목표
Betman과 유사한 스포츠 배팅 플랫폼의 백엔드 시스템 구축

### 1.2 기술 스택
- **Framework**: FastAPI
- **Database**: MySQL
- **Cache/Session**: Redis
- **Authentication**: 아이디/비밀번호 + JWT
- **Password Hashing**: bcrypt
- **Architecture**: DDD (Domain-Driven Design)

---

## 2. 시스템 아키텍처

### 2.1 DDD 레이어 구조
```
src/
├── domain/              # 도메인 계층
│   ├── user/
│   │   ├── entity.py
│   │   ├── repository.py (interface)
│   │   └── service.py
│   ├── betting/
│   │   ├── entity.py
│   │   ├── repository.py
│   │   └── service.py
│   ├── game/
│   │   ├── entity.py
│   │   ├── repository.py
│   │   └── service.py
│   ├── wallet/
│   │   ├── entity.py
│   │   ├── repository.py
│   │   └── service.py
│   └── common/
│       ├── value_objects.py
│       └── exceptions.py
│
├── application/         # 애플리케이션 계층
│   ├── user/
│   │   ├── dto.py
│   │   └── use_cases.py
│   ├── betting/
│   │   ├── dto.py
│   │   └── use_cases.py
│   ├── game/
│   │   ├── dto.py
│   │   └── use_cases.py
│   └── wallet/
│       ├── dto.py
│       └── use_cases.py
│
├── infrastructure/      # 인프라스트럭처 계층
│   ├── database/
│   │   ├── mysql.py
│   │   ├── repositories/
│   │   │   ├── user_repository.py
│   │   │   ├── betting_repository.py
│   │   │   ├── game_repository.py
│   │   │   └── wallet_repository.py
│   │   └── models.py
│   ├── cache/
│   │   └── redis_client.py
│   ├── auth/
│   │   ├── password_hasher.py
│   │   ├── jwt_handler.py
│   │   └── token_repository.py
│   └── external/
│       └── sports_api.py
│
└── presentation/        # 프레젠테이션 계층
    ├── api/
    │   ├── v1/
    │   │   ├── auth.py
    │   │   ├── users.py
    │   │   ├── games.py
    │   │   ├── betting.py
    │   │   └── wallet.py
    │   └── dependencies.py
    ├── schemas/
    │   ├── auth.py
    │   ├── user.py
    │   ├── game.py
    │   ├── betting.py
    │   └── wallet.py
    └── middleware/
        ├── auth.py
        └── error_handler.py
```

---

## 3. 도메인 모델 설계

### 3.1 User (사용자)
```python
# 주요 속성
- user_id: UUID
- username: str  # 로그인 아이디
- password_hash: str  # bcrypt 해시
- email: str
- nickname: str
- role: Enum (user, admin)  # 사용자 권한
- daily_limit: Decimal  # 일일 배팅 한도 (기본 100,000원)
- today_total_bet: Decimal  # 오늘 총 배팅 금액
- last_bet_date: date  # 마지막 배팅 날짜
- created_at: datetime
- updated_at: datetime
- is_active: bool
- is_restricted: bool  # 자가 제한 여부
```

### 3.2 League (리그)
```python
# 주요 속성
- league_id: UUID
- league_name: str
- sport_type: Enum (축구, 야구, 농구, 배구)
- country: str
- is_active: bool
```

### 3.3 Game (경기)
```python
# 주요 속성
- game_id: UUID
- league_id: UUID
- external_id: str  # 외부 스포츠 API의 경기 ID (자동 정산용)
- sport_type: Enum (축구, 야구, 농구, 배구)
- home_team: str
- away_team: str
- start_time: datetime
- status: Enum (예정, 라이브, 마감, 종료, 취소)
- final_score_home: int
- final_score_away: int
- betting_deadline: datetime
- is_live: bool  # 실시간 경기 여부
- created_at: datetime
- updated_at: datetime
```

### 3.4 BettingOption (배팅 옵션)
```python
# 주요 속성
- option_id: UUID
- game_id: UUID
- option_type: Enum (승무패, 핸디캡, 언오버, 승자예상)
- option_name: str  # 예: "홈팀 승", "무승부", "원정팀 승", "홈팀", "원정팀" 등
- odds: Decimal
- handicap_value: Decimal (핸디캡인 경우)
- over_under_line: Decimal (언오버인 경우)
- is_active: bool

# 참고:
# - 승무패: 축구 등 (승/무/패 3가지 옵션)
# - 승패: 야구, 배구 등 무승부가 없는 스포츠 (승/패 2가지 옵션만)
# - option_type은 동일하게 "승무패"로 저장하고, option_name으로 구분
```

### 3.5 Favorite (즐겨찾기)
```python
# 주요 속성
- favorite_id: UUID
- user_id: UUID
- game_id: UUID
- created_at: datetime
```

### 3.6 Bet (배팅)
```python
# 주요 속성
- bet_id: UUID
- user_id: UUID
- bet_type: Enum (단일, 조합)
- total_amount: Decimal
- potential_return: Decimal
- total_odds: Decimal  # 조합 배팅의 총 배당률
- status: Enum (대기, 적중, 미적중, 취소)
- created_at: datetime
```

### 3.7 BetSlip (배팅 슬립)
```python
# 주요 속성
- slip_id: UUID
- bet_id: UUID
- game_id: UUID
- option_id: UUID
- odds: Decimal
- result: Enum (대기, 적중, 미적중)
```

### 3.8 Wallet (지갑)
```python
# 주요 속성
- wallet_id: UUID
- user_id: UUID
- balance: Decimal
- updated_at: datetime
```

### 3.9 Transaction (거래 내역)
```python
# 주요 속성
- transaction_id: UUID
- wallet_id: UUID
- transaction_type: Enum (충전, 출금, 배팅, 환급)
- amount: Decimal
- balance_after: Decimal
- created_at: datetime
```

---

## 4. 주요 기능 명세

### 4.1 인증/인가 (Authentication/Authorization)

#### 4.1.1 회원가입
- **Endpoint**: `POST /api/v1/auth/register`
- **Request Body**:
```json
{
  "username": "user123",
  "password": "password123!",
  "email": "user@example.com",
  "nickname": "닉네임"
}
```
- **비즈니스 로직**:
  1. username 중복 확인
  2. email 중복 확인
  3. 비밀번호 유효성 검증 (최소 8자, 영문/숫자/특수문자 조합)
  4. bcrypt로 비밀번호 해싱
  5. 사용자 생성:
     - role: 'user' (기본값)
     - daily_limit: 100,000원
  6. 지갑 생성 (초기 잔액 0원)
- **Response**: 사용자 정보 (비밀번호 제외)

**참고: 관리자 계정 생성**
- 최초 관리자는 DB에 직접 INSERT 또는 스크립트로 생성
- 또는 환경변수로 ADMIN_USERNAME 설정 시 첫 회원가입을 admin으로 생성

#### 4.1.2 로그인
- **Endpoint**: `POST /api/v1/auth/login`
- **Request Body**:
```json
{
  "username": "user123",
  "password": "password123!"
}
```
- **비즈니스 로직**:
  1. username으로 사용자 조회
  2. bcrypt로 비밀번호 검증
  3. Access Token (JWT, 15분) + Refresh Token (UUID, 7일) 발급
  4. Refresh Token을 Redis에 저장 (key: user_id, value: token, TTL: 7일)
- **Response**:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "uuid...",
  "token_type": "Bearer",
  "user": {
    "user_id": "uuid",
    "username": "user123",
    "email": "user@example.com",
    "nickname": "닉네임"
  }
}
```

#### 4.1.3 Token 갱신
- **Endpoint**: `POST /api/v1/auth/refresh`
- **Request Body**:
```json
{
  "refresh_token": "uuid..."
}
```
- **비즈니스 로직**:
  1. Refresh Token 검증 (Redis 조회)
  2. 유효하면 새로운 Access Token 발급
  3. Refresh Token도 갱신 (선택사항)

#### 4.1.4 로그아웃
- **Endpoint**: `POST /api/v1/auth/logout`
- **Flow**:
  1. Redis에서 Refresh Token 삭제
  2. Access Token Blacklist에 추가

#### 4.1.5 비밀번호 변경
- **Endpoint**: `PUT /api/v1/auth/password`
- **Request Body**:
```json
{
  "current_password": "oldpass123!",
  "new_password": "newpass123!"
}
```
- **비즈니스 로직**:
  1. 현재 비밀번호 검증
  2. 새 비밀번호 유효성 검증
  3. bcrypt로 해싱 후 저장

### 4.2 사용자 관리 (User Management)

#### 4.2.1 프로필 조회
- **Endpoint**: `GET /api/v1/users/me`

#### 4.2.2 프로필 수정
- **Endpoint**: `PATCH /api/v1/users/me`
- **Request Body**:
```json
{
  "nickname": "새닉네임",
  "email": "newemail@example.com"
}
```
- 수정 가능 필드: nickname, email

#### 4.2.3 일일 배팅 한도 조회
- **Endpoint**: `GET /api/v1/users/me/daily-limit`
- **Response**:
```json
{
  "daily_limit": 100000,
  "today_total_bet": 35000,
  "remaining_limit": 65000,
  "last_bet_date": "2024-01-15"
}
```

#### 4.2.4 일일 배팅 한도 설정
- **Endpoint**: `PUT /api/v1/users/me/daily-limit`
- **Request Body**:
```json
{
  "daily_limit": 50000
}
```
- **비즈니스 로직**:
  1. 최소 한도: 10,000원
  2. 최대 한도: 1,000,000원
  3. 즉시 적용

#### 4.2.5 자가 제한 설정
- **Endpoint**: `POST /api/v1/users/me/restriction`
- **Request Body**:
```json
{
  "restriction_type": "휴식기간",
  "duration_days": 30
}
```
- 제한 타입: 휴식 기간

### 4.3 리그 관리 (League Management)

#### 4.3.1 리그 목록 조회
- **Endpoint**: `GET /api/v1/leagues`
- **Query Params**: sport_type, is_active, page, limit
- **Response**: 리그 목록

### 4.4 경기 관리 (Game Management)

#### 4.4.1 구매 가능 경기 목록
- **Endpoint**: `GET /api/v1/games/available`
- **Query Params**:
  - sport_type (스포츠 종류)
  - league_id (리그 필터)
  - bet_type (승무패, 핸디캡, 언오버, 승자예상)
  - date (날짜)
  - page, limit (페이지네이션)
- **Response**: 배팅 마감 전 경기 목록 + 배팅 옵션

#### 4.4.2 마감 경기 목록
- **Endpoint**: `GET /api/v1/games/closed`
- **Query Params**: sport_type, league_id, date, page, limit

#### 4.4.3 경기 상세 정보
- **Endpoint**: `GET /api/v1/games/{game_id}`
- **Response**: 경기 정보 + 배팅 옵션 + 현재 odds

#### 4.4.4 실시간 경기 목록
- **Endpoint**: `GET /api/v1/games/live`
- **Response**: 진행 중인 경기의 실시간 점수 및 상태

#### 4.4.5 즐겨찾기 경기 조회
- **Endpoint**: `GET /api/v1/games/favorites`
- **Response**: 사용자가 즐겨찾기한 경기 목록

#### 4.4.6 경기 결과 업데이트 (관리자 전용)
- **Endpoint**: `PUT /api/v1/games/{game_id}/result`
- **Request Body**:
```json
{
  "status": "종료",
  "final_score_home": 2,
  "final_score_away": 1
}
```
- **비즈니스 로직**:
  1. 경기 상태를 '종료'로 변경
  2. 최종 점수 저장 (final_score_home, final_score_away)
  3. 해당 경기와 관련된 모든 배팅 결과 정산 트리거

#### 4.4.7 경기 상태 변경 (관리자 전용)
- **Endpoint**: `PATCH /api/v1/games/{game_id}/status`
- **Request Body**:
```json
{
  "status": "라이브"
}
```
- 경기 상태: 예정 → 라이브 → 종료
- 또는 예정 → 취소

### 4.5 즐겨찾기 (Favorites)

#### 4.5.1 즐겨찾기 추가
- **Endpoint**: `POST /api/v1/favorites`
- **Request Body**:
```json
{
  "game_id": "uuid"
}
```

#### 4.5.2 즐겨찾기 삭제
- **Endpoint**: `DELETE /api/v1/favorites/{game_id}`

#### 4.5.3 즐겨찾기 목록
- **Endpoint**: `GET /api/v1/favorites`
- **Response**: 즐겨찾기한 경기 목록

### 4.6 배팅 (Betting)

#### 4.6.1 배팅 생성
- **Endpoint**: `POST /api/v1/bets`
- **Request Body**:
```json
{
  "bet_type": "single" | "combo",
  "amount": 10000,
  "selections": [
    {
      "game_id": "uuid",
      "option_id": "uuid"
    }
  ]
}
```
- **비즈니스 로직**:
  1. 사용자 일일 배팅 한도 확인
     - 오늘 날짜와 last_bet_date 비교
     - 날짜가 다르면 today_total_bet을 0으로 초기화
     - today_total_bet + amount <= daily_limit 검증
  2. 사용자 지갑 잔액 확인 (amount <= balance)
  3. 배팅 마감 시간 검증
  4. 배팅 옵션 활성화 여부 확인
  5. 조합 배팅인 경우 총 odds 계산
  6. 트랜잭션으로 처리:
     - 지갑에서 차감
     - 배팅 생성
     - today_total_bet 증가
     - last_bet_date 업데이트

#### 4.6.2 배팅 내역 조회
- **Endpoint**: `GET /api/v1/bets`
- **Query Params**: status, start_date, end_date, page, limit

#### 4.6.3 배팅 상세 조회
- **Endpoint**: `GET /api/v1/bets/{bet_id}`

#### 4.6.4 배팅 취소
- **Endpoint**: `DELETE /api/v1/bets/{bet_id}`
- **조건**: 경기 시작 전, 배팅 생성 후 5분 이내

#### 4.6.5 배팅 결과 정산 (시스템 내부)
- **트리거**: 경기 결과 업데이트 시 (4.4.6 호출 시)
- **비즈니스 로직**:
  1. 해당 경기의 모든 BetSlip 조회 (status = '대기')
  2. 각 BetSlip의 결과 판정:
     - **승무패**: final_score로 승/무/패 판정
     - **핸디캡**: 핸디캡 적용 후 승패 판정
     - **언오버**: 총 득점이 기준선 초과/미만 판정
     - **승자예상**: 토너먼트 종료 시 판정
  3. BetSlip의 result 업데이트 (적중/미적중)
  4. 각 Bet의 모든 BetSlip 결과 확인:
     - **단일 배팅**: BetSlip 1개의 결과
     - **조합 배팅**: 모든 BetSlip이 적중해야 적중
  5. Bet의 status 업데이트 (적중/미적중)
  6. 적중한 경우:
     - potential_return을 사용자 지갑에 환급
     - Transaction 생성 (type: '환급')
  7. 미적중한 경우: 환급 없음

#### 4.6.6 배팅 결과 정산 실행 (관리자 전용)
- **Endpoint**: `POST /api/v1/bets/settle/{game_id}`
- **비즈니스 로직**:
  - 특정 경기에 대한 수동 정산 실행
  - 자동 정산 실패 시 재실행 용도

### 4.7 지갑 관리 (Wallet Management)

#### 4.7.1 잔액 조회
- **Endpoint**: `GET /api/v1/wallet/balance`

#### 4.7.2 충전
- **Endpoint**: `POST /api/v1/wallet/deposit`
- **Request Body**:
```json
{
  "amount": 50000,
  "payment_method": "card" | "bank_transfer"
}
```

#### 4.7.3 출금
- **Endpoint**: `POST /api/v1/wallet/withdraw`
- **Request Body**:
```json
{
  "amount": 30000,
  "bank_account": "110-123-456789"
}
```

#### 4.7.4 거래 내역
- **Endpoint**: `GET /api/v1/wallet/transactions`
- **Query Params**: transaction_type, start_date, end_date, page, limit

---

## 5. 데이터베이스 스키마

### 5.1 MySQL 테이블

#### users
```sql
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    daily_limit DECIMAL(15, 2) DEFAULT 100000.00,
    today_total_bet DECIMAL(15, 2) DEFAULT 0.00,
    last_bet_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_restricted BOOLEAN DEFAULT FALSE,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
);
```

#### leagues
```sql
CREATE TABLE leagues (
    id CHAR(36) PRIMARY KEY,
    league_name VARCHAR(100) NOT NULL,
    sport_type ENUM('축구', '야구', '농구', '배구') NOT NULL,
    country VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sport_type (sport_type),
    INDEX idx_is_active (is_active)
);
```

#### games
```sql
CREATE TABLE games (
    id CHAR(36) PRIMARY KEY,
    league_id CHAR(36) NOT NULL,
    external_id VARCHAR(100),  -- 외부 스포츠 API의 경기 ID (자동 정산용)
    sport_type ENUM('축구', '야구', '농구', '배구') NOT NULL,
    home_team VARCHAR(100) NOT NULL,
    away_team VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    status ENUM('예정', '라이브', '마감', '종료', '취소') DEFAULT '예정',
    final_score_home INT,
    final_score_away INT,
    betting_deadline TIMESTAMP NOT NULL,
    is_live BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (league_id) REFERENCES leagues(id),
    INDEX idx_league_id (league_id),
    INDEX idx_external_id (external_id),
    INDEX idx_sport_type (sport_type),
    INDEX idx_start_time (start_time),
    INDEX idx_status (status),
    INDEX idx_is_live (is_live)
);
```

#### betting_options
```sql
CREATE TABLE betting_options (
    id CHAR(36) PRIMARY KEY,
    game_id CHAR(36) NOT NULL,
    option_type ENUM('승무패', '핸디캡', '언오버', '승자예상') NOT NULL,
    option_name VARCHAR(100) NOT NULL,  -- 예: "홈팀 승", "무승부", "원정팀 승", "오버", "언더" 등
    odds DECIMAL(10, 2) NOT NULL,
    handicap_value DECIMAL(5, 2),  -- 핸디캡인 경우만 사용
    over_under_line DECIMAL(5, 2),  -- 언오버인 경우만 사용
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
    INDEX idx_game_id (game_id),
    INDEX idx_option_type (option_type)
);

-- 참고:
-- 승무패 타입:
--   - 무승부 있음 (축구): option_name이 "홈팀 승", "무승부", "원정팀 승" (3개)
--   - 무승부 없음 (야구, 배구): option_name이 "홈팀", "원정팀" (2개)
-- 각 경기마다 스포츠 특성에 맞는 옵션 개수만 생성
```

#### favorites
```sql
CREATE TABLE favorites (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    game_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_game (user_id, game_id),
    INDEX idx_user_id (user_id),
    INDEX idx_game_id (game_id)
);
```

#### bets
```sql
CREATE TABLE bets (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    bet_type ENUM('단일', '조합') NOT NULL,
    total_amount DECIMAL(15, 2) NOT NULL,
    potential_return DECIMAL(15, 2) NOT NULL,
    total_odds DECIMAL(10, 2) NOT NULL,
    status ENUM('대기', '적중', '미적중', '취소') DEFAULT '대기',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);
```

#### bet_slips
```sql
CREATE TABLE bet_slips (
    id CHAR(36) PRIMARY KEY,
    bet_id CHAR(36) NOT NULL,
    game_id CHAR(36) NOT NULL,
    option_id CHAR(36) NOT NULL,
    odds DECIMAL(10, 2) NOT NULL,
    result ENUM('대기', '적중', '미적중') DEFAULT '대기',
    FOREIGN KEY (bet_id) REFERENCES bets(id) ON DELETE CASCADE,
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (option_id) REFERENCES betting_options(id),
    INDEX idx_bet_id (bet_id),
    INDEX idx_game_id (game_id)
);
```

#### wallets
```sql
CREATE TABLE wallets (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) UNIQUE NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);
```

#### transactions
```sql
CREATE TABLE transactions (
    id CHAR(36) PRIMARY KEY,
    wallet_id CHAR(36) NOT NULL,
    transaction_type ENUM('충전', '출금', '배팅', '환급') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    balance_after DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wallet_id) REFERENCES wallets(id) ON DELETE CASCADE,
    INDEX idx_wallet_id (wallet_id),
    INDEX idx_created_at (created_at)
);
```

### 5.2 Redis 데이터 구조

#### Refresh Token 저장
```
Key: refresh_token:{user_id}
Value: {token_string}
TTL: 604800 seconds (7일)
```

#### Access Token Blacklist (로그아웃 시)
```
Key: blacklist:{access_token}
Value: 1
TTL: 900 seconds (15분, access token 만료 시간)
```

#### Live Game Scores Cache
```
Key: live_game:{game_id}
Value: {score_data_json}
TTL: 10 seconds
```

#### Odds Cache
```
Key: odds:{game_id}
Value: {odds_data_json}
TTL: 30 seconds
```

#### 최근 경기 캐시 (최근 3일)
```
Key: recent_games:{YYYY-MM-DD}
Value: {games_data_json}
TTL: 259200 seconds (3일)
```

---

## 6. 보안 고려사항

### 6.1 비밀번호 보안
- **Hashing Algorithm**: bcrypt
- **Cost Factor**: 12 rounds
- **최소 비밀번호 요구사항**:
  - 최소 8자 이상
  - 영문, 숫자, 특수문자 조합 필수
- **비밀번호 변경 시 기존 비밀번호 검증 필수**

### 6.2 JWT 설정
- **Algorithm**: HS256
- **Access Token Expiry**: 15분
- **Refresh Token Expiry**: 7일
- **Payload**: user_id, username, email, role, iat, exp
- **Secret Key**: 환경변수로 관리, 프로덕션에서 강력한 키 사용 필수

### 6.3 API 보호
- Access Token을 Bearer 토큰으로 헤더에 포함
- Refresh Token은 Redis에 저장 및 검증
- 로그아웃 시 Access Token Blacklist 처리
- 민감한 엔드포인트는 rate limiting 적용
- CORS 설정

### 6.4 권한 관리
- **사용자 권한**: user, admin
- **관리자 전용 API**:
  - `PUT /api/v1/games/{game_id}/result` - 경기 결과 업데이트
  - `PATCH /api/v1/games/{game_id}/status` - 경기 상태 변경
  - `POST /api/v1/bets/settle/{game_id}` - 배팅 결과 수동 정산
- **권한 검증**: JWT 토큰의 role 필드로 확인
- **미들웨어**: @require_role("admin") 데코레이터 사용

### 6.5 데이터 보호
- 비밀번호는 bcrypt로 해싱하여 저장 (절대 평문 저장 금지)
- 금융 거래는 트랜잭션으로 원자성 보장
- SQL Injection 방지 (ORM 사용)
- XSS, CSRF 공격 방지

### 6.6 일일 한도 보안
- 서버 측에서 일일 한도 검증 (클라이언트 우회 방지)
- 동시 요청 처리 시 Race Condition 방지 (트랜잭션 격리 수준 설정)
- 날짜 변경 시 자동 초기화

---

## 7. 배포 및 환경 설정

### 7.1 Docker Compose
- **컨테이너 구성**: FastAPI 애플리케이션, MySQL, Redis
- **개발 환경**: docker-compose.yml을 통한 로컬 개발 환경 구축
- **프로덕션 환경**: docker-compose.prod.yml을 통한 배포

### 7.2 환경 변수
```env
# Database
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DATABASE=betting_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Password Hashing
BCRYPT_ROUNDS=12

# Daily Limit
DEFAULT_DAILY_LIMIT=100000

# App
APP_ENV=development
DEBUG=True
```

### 7.3 의존성 (requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
mysqlclient==2.2.0
redis==5.0.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
httpx==0.25.1

# 스케줄러 (배경 작업)
celery==5.3.4
redis==5.0.1  # Celery 브로커로 Redis 사용

# 또는
apscheduler==3.10.4

# 외부 API 연동 (선택사항)
# requests==2.31.0
# httpx==0.25.1 (이미 포함)
```

---

## 8. 개발 우선순위

### Phase 1: 기본 인프라
1. 프로젝트 구조 설정
2. Docker Compose 환경 구축
   - Dockerfile 작성 (FastAPI 애플리케이션)
   - docker-compose.yml 작성 (MySQL, Redis, FastAPI)
   - 환경 변수 설정 (.env)
3. MySQL, Redis 컨테이너 연결 확인
4. DDD 레이어 기본 구조 생성

### Phase 2: 인증 시스템
1. 회원가입/로그인 (아이디/비밀번호)
2. bcrypt 비밀번호 해싱
3. JWT 발급/검증
4. Refresh Token Redis 저장
5. 비밀번호 변경 기능

### Phase 3: 핵심 도메인
1. User 도메인
2. Wallet 도메인
3. League 도메인
4. Game 도메인
5. Betting 도메인
6. Favorite 도메인

### Phase 4: API 구현
1. Auth API
2. User API
3. League API
4. Game API (필터링 포함)
5. Favorite API
6. Betting API
7. Wallet API

### Phase 5: 고급 기능
1. 실시간 스코어 (Redis 캐싱)
2. 배당률 변동 모니터링
3. **배팅 결과 자동 정산**
   - 경기 종료 자동 감지
   - 배팅 결과 판정 (승무패, 핸디캡, 언오버)
   - 적중 시 자동 환급
   - 경기 취소 시 자동 환불
4. **외부 스포츠 API 연동**
   - 경기 일정 자동 수집
   - 실시간 경기 상태 업데이트
   - 최종 점수 자동 업데이트
5. **스케줄러 (Celery/APScheduler)**
   - 주기적 경기 상태 확인
   - 일일 한도 자동 초기화 (자정)
6. 통계 및 리포트

### Phase 6: 성능 최적화
1. Redis 캐싱 전략 (경기, 배당률)
2. 데이터베이스 쿼리 최적화
3. API 응답 속도 개선
4. 동시성 처리 최적화

---

## 9. 테스트 전략

### 9.1 단위 테스트
- 도메인 로직 테스트
- Use Case 테스트

### 9.2 통합 테스트
- API 엔드포인트 테스트
- 데이터베이스 통합 테스트

### 9.3 E2E 테스트
- 주요 사용자 시나리오 테스트

---

## 10. 참고사항

### 10.1 DDD 패턴 적용
- **Entity**: 고유 식별자를 가진 도메인 객체
- **Value Object**: 식별자 없는 불변 객체
- **Repository**: 데이터 접근 추상화
- **Service**: 도메인 로직 캡슐화
- **Use Case**: 애플리케이션 비즈니스 로직

### 10.2 트랜잭션 관리
- 배팅 생성 시 지갑 차감과 배팅 생성을 하나의 트랜잭션으로 처리
- 배팅 정산 시 지갑 증가와 배팅 상태 업데이트를 하나의 트랜잭션으로 처리

### 10.3 확장성 고려
- 마이크로서비스로 전환 가능한 구조
- 도메인별 독립적인 모듈
- 이벤트 기반 아키텍처 도입 가능성

### 10.4 즐겨찾기 구현 노트
- 사용자당 즐겨찾기 제한 없음
- 경기 시작 후에도 즐겨찾기 유지
- 경기 종료 후 자동 삭제 여부는 정책에 따라 결정

### 10.5 실시간 기능 구현 노트
- 라이브 경기 스코어: Redis 캐싱 (10초 TTL)
- 배당률 변동: Redis 캐싱 (30초 TTL)
- WebSocket 고려 (추후 확장)

### 10.6 일일 배팅 한도 관리
- **기본 한도**: 100,000원
- **최소 한도**: 10,000원
- **최대 한도**: 1,000,000원
- **한도 초기화**: 매일 자정 (날짜 변경 시 today_total_bet = 0)
- **검증 시점**: 배팅 생성 시
- **트랜잭션 처리**: 배팅 금액 차감과 today_total_bet 증가를 하나의 트랜잭션으로 처리
- **Race Condition 방지**:
  - SELECT FOR UPDATE 사용
  - 또는 낙관적 잠금(Optimistic Locking) 사용

### 10.7 비밀번호 정책
- **최소 길이**: 8자
- **복잡도**: 영문, 숫자, 특수문자 조합 필수
- **해싱**: bcrypt (12 rounds)
- **변경 시 검증**: 기존 비밀번호 확인 필수
- **저장**: 절대 평문 저장 금지

### 10.8 배팅 옵션 타입별 특성
**승무패**
- 무승부가 있는 스포츠 (축구 등): 3가지 옵션
  - "홈팀 승", "무승부", "원정팀 승"
- 무승부가 없는 스포츠 (야구, 배구 등): 2가지 옵션만
  - "홈팀", "원정팀" 또는 "홈팀 승", "원정팀 승"
- option_type은 동일하게 "승무패"로 저장
- option_name으로 실제 선택지 구분

**핸디캡**
- handicap_value에 핸디캡 수치 저장
- 예: -1.5, +0.5 등

**언오버 (Over/Under)**
- over_under_line에 기준 점수 저장
- 예: 2.5, 3.5 등
- "오버", "언더" 2가지 옵션

**승자예상**
- 특정 리그나 토너먼트의 최종 우승자 예측
- 여러 팀 중 선택

### 10.9 경기 종료 확인 및 정산 프로세스

#### 경기 종료 확인 방법 (권장: 자동화)

**🎯 추천 방식: 완전 자동화 (관리자 개입 불필요)**

스케줄러(Celery/APScheduler)가 백그라운드에서 자동 실행:

```python
# 스케줄러 작업 (매 1-5분마다 실행)
@scheduler.task(interval=minutes(3))
def check_and_settle_games():
    # 1. 진행 중(라이브) 또는 예정 경기 조회
    games = get_games(status__in=['라이브', '예정'])

    for game in games:
        # 2. 외부 스포츠 API로 경기 상태 확인
        external_data = fetch_game_status(game.external_id)

        # 3. 경기가 종료되었으면
        if external_data.status == 'finished':
            # 경기 정보 업데이트
            game.status = '종료'
            game.final_score_home = external_data.home_score
            game.final_score_away = external_data.away_score
            game.save()

            # 4. 자동으로 배팅 정산 실행
            settle_bets_for_game(game.id)

        # 경기가 시작되었으면
        elif external_data.status == 'live' and game.status == '예정':
            game.status = '라이브'
            game.is_live = True
            game.save()
```

**외부 스포츠 API 예시:**
- **Sportradar** (유료, 신뢰성 높음)
- **The Odds API** (무료 티어 있음)
- **API-Football** (축구 전용)
- **API-Basketball**, **API-Baseball** 등

**장점:**
- ✅ 관리자 개입 불필요
- ✅ 실시간 자동 정산
- ✅ 인적 오류 방지
- ✅ 24시간 자동 운영

---

**🔧 보조 방식: 관리자 수동 업데이트 (예외 상황용)**

다음과 같은 경우에만 사용:
- 외부 API 장애 발생 시
- API가 특정 경기 데이터를 제공하지 않을 때
- 경기 결과에 이의가 있어 수동 조정이 필요한 경우

```
PUT /api/v1/games/{game_id}/result
```

**비즈니스 로직:**
1. 관리자 권한 확인
2. 경기 상태를 '종료'로 변경
3. 최종 점수 입력
4. 배팅 결과 정산 트리거 (자동 방식과 동일)

#### 배팅 결과 정산 로직
```python
# 의사 코드
def settle_game(game_id):
    game = get_game(game_id)
    if game.status != '종료':
        return

    # 1. 해당 경기의 모든 BetSlip 조회
    bet_slips = get_bet_slips_by_game(game_id, status='대기')

    for slip in bet_slips:
        option = get_betting_option(slip.option_id)

        # 2. 결과 판정
        if option.option_type == '승무패':
            slip.result = judge_win_draw_lose(game, option)
        elif option.option_type == '핸디캡':
            slip.result = judge_handicap(game, option)
        elif option.option_type == '언오버':
            slip.result = judge_over_under(game, option)

        slip.save()

    # 3. Bet 결과 확인
    bets = get_unique_bets_from_slips(bet_slips)

    for bet in bets:
        all_slips = get_bet_slips_by_bet(bet.id)

        if bet.bet_type == '단일':
            bet.status = all_slips[0].result  # 적중 또는 미적중
        elif bet.bet_type == '조합':
            # 모든 슬립이 적중해야 적중
            if all(slip.result == '적중' for slip in all_slips):
                bet.status = '적중'
            else:
                bet.status = '미적중'

        # 4. 적중 시 환급
        if bet.status == '적중':
            refund_to_wallet(bet.user_id, bet.potential_return)

        bet.save()
```

#### 경기 취소 처리
- 경기가 '취소'된 경우:
  1. 해당 경기의 모든 Bet의 status를 '취소'로 변경
  2. 배팅 금액(total_amount)을 사용자 지갑에 환불
  3. Transaction 생성 (type: '환급')
  4. today_total_bet에서 차감 (일일 한도 복구)

### 10.10 필터링 및 검색
- 스포츠 종류별 필터
- 리그별 필터
- 배팅 타입별 필터 (승무패, 핸디캡, 언오버, 승자예상)
- 날짜 범위 필터
- 복합 필터 지원