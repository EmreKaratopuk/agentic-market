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


class DocSearchResult(BaseModel):
    """A single semantic search result."""

    content: str = Field(description="Retrieved text chunk")
    source: str = Field(description="Source document filename")
    score: float = Field(description="Similarity score (0–1)")


class DocSearchSuccess(BaseModel):
    """Successful knowledge base search result."""

    success: Literal[True] = True
    results: list[DocSearchResult] = Field(description="Retrieved chunks")


class DocSearchError(BaseModel):
    """Failed knowledge base search result."""

    success: Literal[False] = False
    error: str = Field(description="Error message")


DocSearchQueryResult = DocSearchSuccess | DocSearchError
