"""Knowledge base search tool for policy and FAQ documents."""

import chainlit as cl

from src.schemas import DocSearchError, DocSearchQueryResult, DocSearchSuccess
from src.vectorstore import get_vectorstore


@cl.step(type="tool", name="search_knowledge_base")
async def search_knowledge_base(query: str, k: int = 4) -> DocSearchQueryResult:
    """
    Search the policy and FAQ knowledge base using semantic similarity.

    Scans official marketplace documents for relevant policy details, including
    seller policy, buyer FAQ, shipping SLA, return/refund policy, and
    dispute resolution procedures.

    Args:
        query: Natural language question or topic to search for.
        k: Number of results to return. Defaults to 4.

    Returns:
        DocSearchSuccess with results list, or DocSearchError on failure.

    """
    vs = get_vectorstore()
    try:
        results = vs.similarity_search(query, k=k)
        return DocSearchSuccess(results=results)
    except Exception as e:
        return DocSearchError(error=str(e))
