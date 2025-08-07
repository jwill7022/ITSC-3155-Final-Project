# api/schemas/common.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of records to return")


class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    skip: int
    limit: int
    has_more: bool