-- 데이터베이스 초기화 스크립트
-- Docker Compose로 MySQL 컨테이너 시작 시 자동 실행됨

-- 데이터베이스 생성 (이미 docker-compose에서 생성하지만 명시적으로 작성)
CREATE DATABASE IF NOT EXISTS betting_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE betting_db;

-- 테이블들은 추후 Alembic 마이그레이션으로 생성할 예정
-- 여기서는 기본적인 DB 설정만 수행

-- 타임존 설정
SET time_zone = '+00:00';

-- 초기 설정 완료 메시지
SELECT 'Database initialized successfully' AS message;
