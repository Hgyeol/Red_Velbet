from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    """성공 응답 스키마"""
    message: str = Field("Success", description="응답 메시지")
    status_code: int = Field(200, description="HTTP 상태 코드")
    data: Optional[T] = Field(None, description="응답 데이터")


class PaginationInfo(BaseModel):
    """페이지네이션 정보 스키마"""
    total: int
    page: int
    size: int
    total_pages: int