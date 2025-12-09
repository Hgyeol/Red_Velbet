"""League API 스키마"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class LeagueResponse(BaseModel):
    """리그 응답 스키마"""
    league_id: str
    league_name: str
    sport_type: str
    country: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CreateLeagueRequest(BaseModel):
    """리그 생성 요청 스키마"""
    league_name: str = Field(..., min_length=1, max_length=100, description="리그 이름")
    sport_type: str = Field(..., description="스포츠 종류 (축구, 야구, 농구, 배구)")
    country: str = Field(..., min_length=1, max_length=50, description="국가")
    is_active: bool = Field(default=True, description="활성화 여부")


class UpdateLeagueRequest(BaseModel):
    """리그 업데이트 요청 스키마"""
    league_name: Optional[str] = Field(None, min_length=1, max_length=100, description="리그 이름")
    country: Optional[str] = Field(None, min_length=1, max_length=50, description="국가")
    is_active: Optional[bool] = Field(None, description="활성화 여부")


class PaginationInfo(BaseModel):
    """페이지네이션 정보"""
    page: int
    limit: int
    total: int
    total_pages: int


class LeagueListResponse(BaseModel):
    """리그 목록 응답 스키마"""
    items: list[LeagueResponse]
    pagination: PaginationInfo
