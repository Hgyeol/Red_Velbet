# 배팅 사이트 API 명세서

## 목차
1. [개요](#1-개요)
2. [인증](#2-인증)
3. [공통 사항](#3-공통-사항)
4. [에러 코드](#4-에러-코드)
5. [API 엔드포인트](#5-api-엔드포인트)
   - [5.1 인증 (Authentication)](#51-인증-authentication)
   - [5.2 사용자 (Users)](#52-사용자-users)
   - [5.3 리그 (Leagues)](#53-리그-leagues)
   - [5.4 경기 (Games)](#54-경기-games)
   - [5.5 즐겨찾기 (Favorites)](#55-즐겨찾기-favorites)
   - [5.6 배팅 (Betting)](#56-배팅-betting)
   - [5.7 지갑 (Wallet)](#57-지갑-wallet)

---

## 1. 개요

### Base URL
```
개발 환경: http://localhost:8000
프로덕션: https://api.betting-site.com
```

### API 버전
```
v1: /api/v1
```

### Content-Type
```
application/json
```

---

## 2. 인증

### 인증 방식
- **JWT (JSON Web Token)** 기반 인증
- Access Token과 Refresh Token 사용

### 토큰 유효기간
- **Access Token**: 15분
- **Refresh Token**: 7일

### 인증 헤더
인증이 필요한 API 요청 시 다음 헤더를 포함해야 합니다:
```http
Authorization: Bearer {access_token}
```

### 인증 플로우
1. 회원가입 또는 로그인하여 Access Token과 Refresh Token 받기
2. API 요청 시 Authorization 헤더에 Access Token 포함
3. Access Token 만료 시 Refresh Token으로 갱신
4. Refresh Token도 만료되면 재로그인 필요

---

## 3. 공통 사항

### 요청 헤더
```http
Content-Type: application/json
Authorization: Bearer {access_token}  # 인증이 필요한 경우
```

### 성공 응답 형식
```json
{
  "success": true,
  "data": {
    // 응답 데이터
  }
}
```

### 에러 응답 형식
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "에러 메시지",
    "details": {}  # 선택적
  }
}
```

### 페이지네이션
페이지네이션을 지원하는 API의 응답 형식:
```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "total_pages": 5
    }
  }
}
```

### 쿼리 파라미터 (페이지네이션)
- `page`: 페이지 번호 (기본값: 1)
- `limit`: 페이지당 항목 수 (기본값: 20, 최대: 100)

---

## 4. 에러 코드

### 일반 에러
| 코드 | HTTP Status | 설명 |
|------|-------------|------|
| `INVALID_REQUEST` | 400 | 잘못된 요청 |
| `UNAUTHORIZED` | 401 | 인증 실패 |
| `FORBIDDEN` | 403 | 권한 없음 |
| `NOT_FOUND` | 404 | 리소스를 찾을 수 없음 |
| `CONFLICT` | 409 | 리소스 충돌 (중복 등) |
| `INTERNAL_ERROR` | 500 | 서버 내부 오류 |

### 인증 관련 에러
| 코드 | HTTP Status | 설명 |
|------|-------------|------|
| `INVALID_CREDENTIALS` | 401 | 아이디 또는 비밀번호가 잘못됨 |
| `TOKEN_EXPIRED` | 401 | 토큰이 만료됨 |
| `INVALID_TOKEN` | 401 | 유효하지 않은 토큰 |
| `USER_ALREADY_EXISTS` | 409 | 이미 존재하는 사용자 |

### 배팅 관련 에러
| 코드 | HTTP Status | 설명 |
|------|-------------|------|
| `INSUFFICIENT_BALANCE` | 400 | 잔액 부족 |
| `DAILY_LIMIT_EXCEEDED` | 400 | 일일 배팅 한도 초과 |
| `BETTING_DEADLINE_PASSED` | 400 | 배팅 마감 시간 초과 |
| `INVALID_BET_AMOUNT` | 400 | 잘못된 배팅 금액 |

---

## 5. API 엔드포인트

## 5.1 인증 (Authentication)

### 5.1.1 회원가입
사용자 계정을 생성합니다.

**Endpoint**
```http
POST /api/v1/auth/register
```

**요청 헤더**
```http
Content-Type: application/json
```

**요청 바디**
```json
{
  "username": "user123",
  "password": "password123!",
  "email": "user@example.com",
  "nickname": "닉네임"
}
```

**필드 설명**
- `username` (required): 로그인 아이디 (4-50자, 영문/숫자만 허용)
- `password` (required): 비밀번호 (최소 8자, 영문/숫자/특수문자 조합)
- `email` (required): 이메일 주소
- `nickname` (required): 닉네임 (2-50자)

**성공 응답** (201 Created)
```json
{
  "success": true,
  "data": {
    "user": {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "user123",
      "email": "user@example.com",
      "nickname": "닉네임",
      "daily_limit": 100000,
      "created_at": "2024-01-15T10:30:00Z"
    }
  }
}
```

**에러 응답**
```json
{
  "success": false,
  "error": {
    "code": "USER_ALREADY_EXISTS",
    "message": "이미 존재하는 사용자입니다"
  }
}
```

---

### 5.1.2 로그인
사용자 인증 후 토큰을 발급받습니다.

**Endpoint**
```http
POST /api/v1/auth/login
```

**요청 헤더**
```http
Content-Type: application/json
```

**요청 바디**
```json
{
  "username": "user123",
  "password": "password123!"
}
```

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "550e8400-e29b-41d4-a716-446655440000",
    "token_type": "Bearer",
    "expires_in": 900,
    "user": {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "user123",
      "email": "user@example.com",
      "nickname": "닉네임",
      "role": "user"
    }
  }
}
```

**에러 응답**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "아이디 또는 비밀번호가 잘못되었습니다"
  }
}
```

---

### 5.1.3 토큰 갱신
만료된 Access Token을 Refresh Token으로 갱신합니다.

**Endpoint**
```http
POST /api/v1/auth/refresh
```

**요청 바디**
```json
{
  "refresh_token": "550e8400-e29b-41d4-a716-446655440000"
}
```

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 900
  }
}
```

---

### 5.1.4 로그아웃
현재 세션을 종료합니다.

**Endpoint**
```http
POST /api/v1/auth/logout
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
```

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "message": "로그아웃되었습니다"
  }
}
```

---

### 5.1.5 비밀번호 변경
현재 사용자의 비밀번호를 변경합니다.

**Endpoint**
```http
PUT /api/v1/auth/password
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

**요청 바디**
```json
{
  "current_password": "oldpass123!",
  "new_password": "newpass123!"
}
```

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "message": "비밀번호가 변경되었습니다"
  }
}
```

---

## 5.2 사용자 (Users)

### 5.2.1 내 프로필 조회
현재 로그인한 사용자의 프로필을 조회합니다.

**Endpoint**
```http
GET /api/v1/users/me
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
```

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "user123",
    "email": "user@example.com",
    "nickname": "닉네임",
    "role": "user",
    "daily_limit": 100000,
    "today_total_bet": 35000,
    "last_bet_date": "2024-01-15",
    "is_active": true,
    "is_restricted": false,
    "created_at": "2024-01-01T10:00:00Z"
  }
}
```

---

### 5.2.2 프로필 수정
현재 사용자의 프로필 정보를 수정합니다.

**Endpoint**
```http
PATCH /api/v1/users/me
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

**요청 바디**
```json
{
  "nickname": "새닉네임",
  "email": "newemail@example.com"
}
```

**필드 설명**
- `nickname` (optional): 새 닉네임
- `email` (optional): 새 이메일 주소

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "user123",
    "email": "newemail@example.com",
    "nickname": "새닉네임",
    "updated_at": "2024-01-15T11:30:00Z"
  }
}
```

---

### 5.2.3 일일 배팅 한도 조회
현재 사용자의 일일 배팅 한도 정보를 조회합니다.

**Endpoint**
```http
GET /api/v1/users/me/daily-limit
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
```

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "daily_limit": 100000,
    "today_total_bet": 35000,
    "remaining_limit": 65000,
    "last_bet_date": "2024-01-15"
  }
}
```

**필드 설명**
- `daily_limit`: 일일 배팅 한도 (원)
- `today_total_bet`: 오늘 사용한 배팅 금액 (원)
- `remaining_limit`: 오늘 남은 배팅 한도 (원)
- `last_bet_date`: 마지막 배팅 날짜

---

### 5.2.4 일일 배팅 한도 설정
일일 배팅 한도를 설정합니다.

**Endpoint**
```http
PUT /api/v1/users/me/daily-limit
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

**요청 바디**
```json
{
  "daily_limit": 50000
}
```

**필드 설명**
- `daily_limit` (required): 새 일일 한도 (최소: 10,000원, 최대: 1,000,000원)

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "daily_limit": 50000,
    "message": "일일 배팅 한도가 변경되었습니다"
  }
}
```

---

### 5.2.5 자가 제한 설정
사용자가 스스로 배팅을 제한합니다.

**Endpoint**
```http
POST /api/v1/users/me/restriction
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

**요청 바디**
```json
{
  "restriction_type": "휴식기간",
  "duration_days": 30
}
```

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "is_restricted": true,
    "restriction_end_date": "2024-02-15",
    "message": "자가 제한이 설정되었습니다"
  }
}
```

---

## 5.3 리그 (Leagues)

### 5.3.1 리그 목록 조회
모든 리그 목록을 조회합니다.

**Endpoint**
```http
GET /api/v1/leagues
```

**쿼리 파라미터**
- `sport_type` (optional): 스포츠 종류 (`축구`, `야구`, `농구`, `배구`)
- `is_active` (optional): 활성 여부 (true/false)
- `page` (optional): 페이지 번호 (기본값: 1)
- `limit` (optional): 페이지당 항목 수 (기본값: 20)

**요청 예시**
```http
GET /api/v1/leagues?sport_type=축구&is_active=true&page=1&limit=20
```

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "league_id": "550e8400-e29b-41d4-a716-446655440000",
        "league_name": "프리미어리그",
        "sport_type": "축구",
        "country": "영국",
        "is_active": true,
        "created_at": "2024-01-01T00:00:00Z"
      },
      {
        "league_id": "550e8400-e29b-41d4-a716-446655440001",
        "league_name": "라리가",
        "sport_type": "축구",
        "country": "스페인",
        "is_active": true,
        "created_at": "2024-01-01T00:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 50,
      "total_pages": 3
    }
  }
}
```

---

## 5.4 경기 (Games)

### 5.4.1 구매 가능 경기 목록
배팅 가능한 경기 목록을 조회합니다.

**Endpoint**
```http
GET /api/v1/games/available
```

**쿼리 파라미터**
- `sport_type` (optional): 스포츠 종류 (`축구`, `야구`, `농구`, `배구`)
- `league_id` (optional): 리그 ID
- `bet_type` (optional): 배팅 타입 (`승무패`, `핸디캡`, `언오버`, `승자예상`)
- `date` (optional): 날짜 (YYYY-MM-DD)
- `page` (optional): 페이지 번호
- `limit` (optional): 페이지당 항목 수

**요청 예시**
```http
GET /api/v1/games/available?sport_type=축구&bet_type=승무패&page=1
```

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "game_id": "650e8400-e29b-41d4-a716-446655440000",
        "league": {
          "league_id": "550e8400-e29b-41d4-a716-446655440000",
          "league_name": "프리미어리그"
        },
        "sport_type": "축구",
        "home_team": "맨체스터 유나이티드",
        "away_team": "리버풀",
        "start_time": "2024-01-15T20:00:00Z",
        "status": "예정",
        "betting_deadline": "2024-01-15T19:55:00Z",
        "is_live": false,
        "betting_options": [
          {
            "option_id": "750e8400-e29b-41d4-a716-446655440000",
            "option_type": "승무패",
            "option_name": "홈팀 승",
            "odds": 1.85
          },
          {
            "option_id": "750e8400-e29b-41d4-a716-446655440001",
            "option_type": "승무패",
            "option_name": "무승부",
            "odds": 3.40
          },
          {
            "option_id": "750e8400-e29b-41d4-a716-446655440002",
            "option_type": "승무패",
            "option_name": "원정팀 승",
            "odds": 4.20
          }
        ]
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "total_pages": 3
    }
  }
}
```

---

### 5.4.2 마감 경기 목록
배팅이 마감된 경기 목록을 조회합니다.

**Endpoint**
```http
GET /api/v1/games/closed
```

**쿼리 파라미터**
- `sport_type` (optional): 스포츠 종류
- `league_id` (optional): 리그 ID
- `date` (optional): 날짜 (YYYY-MM-DD)
- `page` (optional): 페이지 번호
- `limit` (optional): 페이지당 항목 수

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "game_id": "650e8400-e29b-41d4-a716-446655440000",
        "league_name": "프리미어리그",
        "sport_type": "축구",
        "home_team": "맨체스터 유나이티드",
        "away_team": "리버풀",
        "start_time": "2024-01-15T20:00:00Z",
        "status": "마감",
        "is_live": false
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 30,
      "total_pages": 2
    }
  }
}
```

---

### 5.4.3 경기 상세 정보
특정 경기의 상세 정보를 조회합니다.

**Endpoint**
```http
GET /api/v1/games/{game_id}
```

**경로 파라미터**
- `game_id` (required): 경기 ID

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "game_id": "650e8400-e29b-41d4-a716-446655440000",
    "league": {
      "league_id": "550e8400-e29b-41d4-a716-446655440000",
      "league_name": "프리미어리그",
      "sport_type": "축구",
      "country": "영국"
    },
    "sport_type": "축구",
    "home_team": "맨체스터 유나이티드",
    "away_team": "리버풀",
    "start_time": "2024-01-15T20:00:00Z",
    "status": "예정",
    "betting_deadline": "2024-01-15T19:55:00Z",
    "is_live": false,
    "final_score_home": null,
    "final_score_away": null,
    "betting_options": {
      "승무패": [
        {
          "option_id": "750e8400-e29b-41d4-a716-446655440000",
          "option_name": "홈팀 승",
          "odds": 1.85
        },
        {
          "option_id": "750e8400-e29b-41d4-a716-446655440001",
          "option_name": "무승부",
          "odds": 3.40
        },
        {
          "option_id": "750e8400-e29b-41d4-a716-446655440002",
          "option_name": "원정팀 승",
          "odds": 4.20
        }
      ],
      "핸디캡": [
        {
          "option_id": "750e8400-e29b-41d4-a716-446655440003",
          "option_name": "홈팀 -1.5",
          "handicap_value": -1.5,
          "odds": 2.10
        },
        {
          "option_id": "750e8400-e29b-41d4-a716-446655440004",
          "option_name": "원정팀 +1.5",
          "handicap_value": 1.5,
          "odds": 1.70
        }
      ],
      "언오버": [
        {
          "option_id": "750e8400-e29b-41d4-a716-446655440005",
          "option_name": "오버 2.5",
          "over_under_line": 2.5,
          "odds": 1.90
        },
        {
          "option_id": "750e8400-e29b-41d4-a716-446655440006",
          "option_name": "언더 2.5",
          "over_under_line": 2.5,
          "odds": 1.85
        }
      ]
    },
    "created_at": "2024-01-10T00:00:00Z",
    "updated_at": "2024-01-14T10:00:00Z"
  }
}
```

---

### 5.4.4 실시간 경기 목록
현재 진행 중인 경기 목록을 조회합니다.

**Endpoint**
```http
GET /api/v1/games/live
```

**쿼리 파라미터**
- `sport_type` (optional): 스포츠 종류
- `page` (optional): 페이지 번호
- `limit` (optional): 페이지당 항목 수

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "game_id": "650e8400-e29b-41d4-a716-446655440000",
        "league_name": "프리미어리그",
        "sport_type": "축구",
        "home_team": "맨체스터 유나이티드",
        "away_team": "리버풀",
        "start_time": "2024-01-15T20:00:00Z",
        "status": "라이브",
        "is_live": true,
        "current_score_home": 1,
        "current_score_away": 1,
        "match_time": "45:00"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 5,
      "total_pages": 1
    }
  }
}
```

---

### 5.4.5 즐겨찾기 경기 조회
사용자가 즐겨찾기한 경기 목록을 조회합니다.

**Endpoint**
```http
GET /api/v1/games/favorites
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
```

**쿼리 파라미터**
- `page` (optional): 페이지 번호
- `limit` (optional): 페이지당 항목 수

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "favorite_id": "850e8400-e29b-41d4-a716-446655440000",
        "game": {
          "game_id": "650e8400-e29b-41d4-a716-446655440000",
          "league_name": "프리미어리그",
          "sport_type": "축구",
          "home_team": "맨체스터 유나이티드",
          "away_team": "리버풀",
          "start_time": "2024-01-15T20:00:00Z",
          "status": "예정"
        },
        "created_at": "2024-01-14T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 8,
      "total_pages": 1
    }
  }
}
```

---

## 5.5 즐겨찾기 (Favorites)

### 5.5.1 즐겨찾기 추가
경기를 즐겨찾기에 추가합니다.

**Endpoint**
```http
POST /api/v1/favorites
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

**요청 바디**
```json
{
  "game_id": "650e8400-e29b-41d4-a716-446655440000"
}
```

**성공 응답** (201 Created)
```json
{
  "success": true,
  "data": {
    "favorite_id": "850e8400-e29b-41d4-a716-446655440000",
    "game_id": "650e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

---

### 5.5.2 즐겨찾기 삭제
즐겨찾기에서 경기를 제거합니다.

**Endpoint**
```http
DELETE /api/v1/favorites/{game_id}
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
```

**경로 파라미터**
- `game_id` (required): 경기 ID

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "message": "즐겨찾기에서 제거되었습니다"
  }
}
```

---

### 5.5.3 즐겨찾기 목록
즐겨찾기한 경기 목록을 조회합니다. (5.4.5와 동일)

**Endpoint**
```http
GET /api/v1/favorites
```

---

## 5.6 배팅 (Betting)

### 5.6.1 배팅 생성
새로운 배팅을 생성합니다.

**Endpoint**
```http
POST /api/v1/bets
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

**요청 바디**
```json
{
  "bet_type": "combo",
  "amount": 10000,
  "selections": [
    {
      "game_id": "650e8400-e29b-41d4-a716-446655440000",
      "option_id": "750e8400-e29b-41d4-a716-446655440000"
    },
    {
      "game_id": "650e8400-e29b-41d4-a716-446655440001",
      "option_id": "750e8400-e29b-41d4-a716-446655440010"
    }
  ]
}
```

**필드 설명**
- `bet_type` (required): 배팅 타입 (`single` | `combo`)
  - `single`: 단일 배팅 (selections 1개)
  - `combo`: 조합 배팅 (selections 2개 이상)
- `amount` (required): 배팅 금액 (원)
- `selections` (required): 선택한 배팅 옵션 목록

**성공 응답** (201 Created)
```json
{
  "success": true,
  "data": {
    "bet_id": "b50e8400-e29b-41d4-a716-446655440000",
    "bet_type": "조합",
    "total_amount": 10000,
    "total_odds": 3.89,
    "potential_return": 38900,
    "status": "대기",
    "bet_slips": [
      {
        "slip_id": "c50e8400-e29b-41d4-a716-446655440000",
        "game": {
          "game_id": "650e8400-e29b-41d4-a716-446655440000",
          "home_team": "맨체스터 유나이티드",
          "away_team": "리버풀"
        },
        "option": {
          "option_id": "750e8400-e29b-41d4-a716-446655440000",
          "option_type": "승무패",
          "option_name": "홈팀 승",
          "odds": 1.85
        },
        "result": "대기"
      },
      {
        "slip_id": "c50e8400-e29b-41d4-a716-446655440001",
        "game": {
          "game_id": "650e8400-e29b-41d4-a716-446655440001",
          "home_team": "바르셀로나",
          "away_team": "레알 마드리드"
        },
        "option": {
          "option_id": "750e8400-e29b-41d4-a716-446655440010",
          "option_type": "승무패",
          "option_name": "원정팀 승",
          "odds": 2.10
        },
        "result": "대기"
      }
    ],
    "created_at": "2024-01-15T10:15:00Z"
  }
}
```

**에러 응답**
```json
{
  "success": false,
  "error": {
    "code": "DAILY_LIMIT_EXCEEDED",
    "message": "일일 배팅 한도를 초과했습니다",
    "details": {
      "daily_limit": 100000,
      "today_total_bet": 95000,
      "remaining_limit": 5000,
      "requested_amount": 10000
    }
  }
}
```

---

### 5.6.2 배팅 내역 조회
사용자의 배팅 내역을 조회합니다.

**Endpoint**
```http
GET /api/v1/bets
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
```

**쿼리 파라미터**
- `status` (optional): 배팅 상태 (`대기`, `적중`, `미적중`, `취소`)
- `start_date` (optional): 시작 날짜 (YYYY-MM-DD)
- `end_date` (optional): 종료 날짜 (YYYY-MM-DD)
- `page` (optional): 페이지 번호
- `limit` (optional): 페이지당 항목 수

**요청 예시**
```http
GET /api/v1/bets?status=대기&start_date=2024-01-01&end_date=2024-01-31&page=1
```

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "bet_id": "b50e8400-e29b-41d4-a716-446655440000",
        "bet_type": "조합",
        "total_amount": 10000,
        "total_odds": 3.89,
        "potential_return": 38900,
        "status": "대기",
        "slip_count": 2,
        "created_at": "2024-01-15T10:15:00Z"
      },
      {
        "bet_id": "b50e8400-e29b-41d4-a716-446655440001",
        "bet_type": "단일",
        "total_amount": 20000,
        "total_odds": 1.85,
        "potential_return": 37000,
        "status": "적중",
        "slip_count": 1,
        "created_at": "2024-01-14T15:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "total_pages": 3
    }
  }
}
```

---

### 5.6.3 배팅 상세 조회
특정 배팅의 상세 정보를 조회합니다.

**Endpoint**
```http
GET /api/v1/bets/{bet_id}
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
```

**경로 파라미터**
- `bet_id` (required): 배팅 ID

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "bet_id": "b50e8400-e29b-41d4-a716-446655440000",
    "bet_type": "조합",
    "total_amount": 10000,
    "total_odds": 3.89,
    "potential_return": 38900,
    "status": "대기",
    "bet_slips": [
      {
        "slip_id": "c50e8400-e29b-41d4-a716-446655440000",
        "game": {
          "game_id": "650e8400-e29b-41d4-a716-446655440000",
          "league_name": "프리미어리그",
          "home_team": "맨체스터 유나이티드",
          "away_team": "리버풀",
          "start_time": "2024-01-15T20:00:00Z",
          "status": "예정",
          "final_score_home": null,
          "final_score_away": null
        },
        "option": {
          "option_id": "750e8400-e29b-41d4-a716-446655440000",
          "option_type": "승무패",
          "option_name": "홈팀 승",
          "odds": 1.85
        },
        "result": "대기"
      },
      {
        "slip_id": "c50e8400-e29b-41d4-a716-446655440001",
        "game": {
          "game_id": "650e8400-e29b-41d4-a716-446655440001",
          "league_name": "라리가",
          "home_team": "바르셀로나",
          "away_team": "레알 마드리드",
          "start_time": "2024-01-15T22:00:00Z",
          "status": "예정",
          "final_score_home": null,
          "final_score_away": null
        },
        "option": {
          "option_id": "750e8400-e29b-41d4-a716-446655440010",
          "option_type": "승무패",
          "option_name": "원정팀 승",
          "odds": 2.10
        },
        "result": "대기"
      }
    ],
    "created_at": "2024-01-15T10:15:00Z"
  }
}
```

---

### 5.6.4 배팅 취소
배팅을 취소하고 금액을 환불받습니다.

**Endpoint**
```http
DELETE /api/v1/bets/{bet_id}
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
```

**경로 파라미터**
- `bet_id` (required): 배팅 ID

**취소 조건**
- 경기 시작 전
- 배팅 생성 후 5분 이내

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "bet_id": "b50e8400-e29b-41d4-a716-446655440000",
    "status": "취소",
    "refunded_amount": 10000,
    "message": "배팅이 취소되고 금액이 환불되었습니다"
  }
}
```

**에러 응답**
```json
{
  "success": false,
  "error": {
    "code": "CANCELLATION_NOT_ALLOWED",
    "message": "배팅 취소 가능 시간(5분)이 지났습니다"
  }
}
```

---

## 5.7 지갑 (Wallet)

### 5.7.1 잔액 조회
현재 사용자의 지갑 잔액을 조회합니다.

**Endpoint**
```http
GET /api/v1/wallet/balance
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
```

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "wallet_id": "d50e8400-e29b-41d4-a716-446655440000",
    "balance": 85000,
    "updated_at": "2024-01-15T10:15:00Z"
  }
}
```

---

### 5.7.2 충전
지갑에 금액을 충전합니다.

**Endpoint**
```http
POST /api/v1/wallet/deposit
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

**요청 바디**
```json
{
  "amount": 50000,
  "payment_method": "card"
}
```

**필드 설명**
- `amount` (required): 충전 금액 (원)
- `payment_method` (required): 결제 수단 (`card` | `bank_transfer`)

**성공 응답** (201 Created)
```json
{
  "success": true,
  "data": {
    "transaction_id": "e50e8400-e29b-41d4-a716-446655440000",
    "wallet_id": "d50e8400-e29b-41d4-a716-446655440000",
    "transaction_type": "충전",
    "amount": 50000,
    "balance_after": 135000,
    "payment_method": "card",
    "created_at": "2024-01-15T10:20:00Z"
  }
}
```

---

### 5.7.3 출금
지갑에서 금액을 출금합니다.

**Endpoint**
```http
POST /api/v1/wallet/withdraw
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

**요청 바디**
```json
{
  "amount": 30000,
  "bank_account": "110-123-456789"
}
```

**필드 설명**
- `amount` (required): 출금 금액 (원)
- `bank_account` (required): 출금 계좌번호

**성공 응답** (201 Created)
```json
{
  "success": true,
  "data": {
    "transaction_id": "e50e8400-e29b-41d4-a716-446655440001",
    "wallet_id": "d50e8400-e29b-41d4-a716-446655440000",
    "transaction_type": "출금",
    "amount": 30000,
    "balance_after": 105000,
    "bank_account": "110-***-***789",
    "created_at": "2024-01-15T10:25:00Z"
  }
}
```

**에러 응답**
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_BALANCE",
    "message": "잔액이 부족합니다",
    "details": {
      "current_balance": 105000,
      "requested_amount": 200000
    }
  }
}
```

---

### 5.7.4 거래 내역
지갑의 거래 내역을 조회합니다.

**Endpoint**
```http
GET /api/v1/wallet/transactions
```

**요청 헤더**
```http
Authorization: Bearer {access_token}
```

**쿼리 파라미터**
- `transaction_type` (optional): 거래 타입 (`충전`, `출금`, `배팅`, `환급`)
- `start_date` (optional): 시작 날짜 (YYYY-MM-DD)
- `end_date` (optional): 종료 날짜 (YYYY-MM-DD)
- `page` (optional): 페이지 번호
- `limit` (optional): 페이지당 항목 수

**요청 예시**
```http
GET /api/v1/wallet/transactions?transaction_type=배팅&start_date=2024-01-01&page=1
```

**성공 응답** (200 OK)
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "transaction_id": "e50e8400-e29b-41d4-a716-446655440000",
        "transaction_type": "충전",
        "amount": 50000,
        "balance_after": 135000,
        "created_at": "2024-01-15T10:20:00Z"
      },
      {
        "transaction_id": "e50e8400-e29b-41d4-a716-446655440001",
        "transaction_type": "배팅",
        "amount": -10000,
        "balance_after": 125000,
        "created_at": "2024-01-15T10:15:00Z"
      },
      {
        "transaction_id": "e50e8400-e29b-41d4-a716-446655440002",
        "transaction_type": "환급",
        "amount": 37000,
        "balance_after": 162000,
        "created_at": "2024-01-14T22:30:00Z"
      },
      {
        "transaction_id": "e50e8400-e29b-41d4-a716-446655440003",
        "transaction_type": "출금",
        "amount": -30000,
        "balance_after": 132000,
        "created_at": "2024-01-14T15:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 78,
      "total_pages": 4
    }
  }
}
```

**필드 설명**
- `amount`: 거래 금액 (양수: 입금, 음수: 출금)
- `balance_after`: 거래 후 잔액

---

## 부록

### A. 배팅 옵션 타입별 특성

#### 승무패
- **무승부 있음 (축구)**: 3가지 옵션
  - "홈팀 승", "무승부", "원정팀 승"
- **무승부 없음 (야구, 배구)**: 2가지 옵션만
  - "홈팀", "원정팀"

#### 핸디캡
- `handicap_value`: 핸디캡 수치 (예: -1.5, +0.5)
- 예: "홈팀 -1.5"는 홈팀이 2골 이상 차이로 이겨야 적중

#### 언오버 (Over/Under)
- `over_under_line`: 기준 점수 (예: 2.5, 3.5)
- "오버 2.5": 총 득점이 3점 이상이면 적중
- "언더 2.5": 총 득점이 2점 이하면 적중

#### 승자예상
- 특정 리그/토너먼트의 최종 우승자 예측
- 여러 팀 중 선택

---

### B. 날짜/시간 형식
- **ISO 8601 형식 사용**: `YYYY-MM-DDTHH:mm:ssZ`
- **타임존**: UTC (Z)
- **날짜만 표시**: `YYYY-MM-DD`

예시:
```
2024-01-15T20:00:00Z  # 2024년 1월 15일 오후 8시 (UTC)
2024-01-15            # 2024년 1월 15일
```

---

### C. 개발 팁

#### 1. 토큰 갱신 처리
Access Token이 만료되면 `401 Unauthorized` 응답과 함께 `TOKEN_EXPIRED` 에러 코드가 반환됩니다. 이 경우 자동으로 Refresh Token으로 갱신하는 로직을 구현하세요.

```javascript
// 예시 (JavaScript)
async function apiCall(url, options) {
  let response = await fetch(url, options);

  if (response.status === 401) {
    const error = await response.json();
    if (error.error.code === 'TOKEN_EXPIRED') {
      // 토큰 갱신
      await refreshAccessToken();
      // 재시도
      response = await fetch(url, options);
    }
  }

  return response;
}
```

#### 2. 일일 한도 체크
배팅 생성 전에 `/api/v1/users/me/daily-limit` 엔드포인트로 남은 한도를 확인하여 사용자에게 표시하세요.

#### 3. 실시간 업데이트
라이브 경기의 경우 주기적으로 `/api/v1/games/live` 또는 `/api/v1/games/{game_id}` 엔드포인트를 polling하여 최신 점수를 업데이트하세요.

---

### D. 문의

API 사용 중 문제가 발생하거나 문의사항이 있으시면 다음으로 연락주세요:
- 이메일: dev@betting-site.com
- 개발자 문서: https://docs.betting-site.com
