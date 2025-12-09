"""도메인 공통 예외"""


class DomainException(Exception):
    """도메인 계층 기본 예외"""
    pass


class EntityNotFoundException(DomainException):
    """엔티티를 찾을 수 없음"""
    pass


class DuplicateEntityException(DomainException):
    """중복된 엔티티"""
    pass


class ValidationException(DomainException):
    """유효성 검증 실패"""
    pass


class AuthenticationException(DomainException):
    """인증 실패"""
    pass


class AuthorizationException(DomainException):
    """권한 없음"""
    pass
