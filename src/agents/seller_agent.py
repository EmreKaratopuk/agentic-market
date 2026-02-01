from functools import lru_cache

import chainlit as cl
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from src.llm import get_llm
from src.prompts import get_seller_prompt
from src.tools.seller import (
    get_seller_performance_rankings,
    get_seller_profile,
    get_seller_stats_all_states,
    get_seller_stats_by_state,
)


@lru_cache
def get_seller_agent():
    return create_agent(
        name="Seller Agent",
        model=get_llm(),
        system_prompt=get_seller_prompt(),
        tools=[
            get_seller_performance_rankings,
            get_seller_profile,
            get_seller_stats_by_state,
            get_seller_stats_all_states,
        ],
    )


async def get_seller_details(query: str, config: RunnableConfig) -> str:
    """
    Get seller information using natural language.

    Use this when the user asks seller-related questions such as seller rankings,
    seller performance metrics, regional seller statistics, or revenue trends.
    This tool takes a natural-language question and replies in natural language
    to provide seller information.

    Input: Natural language question.
    Example: "Who are the top 5 sellers by revenue?"
    Example: "Which states have the most sellers and highest revenue?"
    Example: "What are the monthly revenue trends for the marketplace?"
    """
    async with cl.Step(type="tool", name="get_seller_details") as step:
        result = await get_seller_agent().ainvoke(
            {"messages": [HumanMessage(content=query)]},
            config=config,
        )
        output = result["messages"][-1].text

        step.input = query
        step.output = output

        return output
