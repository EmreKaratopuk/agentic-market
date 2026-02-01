"""Pydantic schemas for tool responses."""

from typing import Literal

from pydantic import BaseModel, Field


class DBQuerySuccess(BaseModel):
    """Successful database query result."""

    success: Literal[True] = True
    rows: list[dict] = Field(description="Query result rows")
    count: int = Field(description="Number of rows returned")


class DBQueryError(BaseModel):
    """Failed database query result."""

    success: Literal[False] = False
    error: str = Field(description="Error message")


DBQueryResult = DBQuerySuccess | DBQueryError
