from functools import lru_cache

import chainlit as cl
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from src.llm import get_llm
from src.prompts import get_customer_prompt
from src.tools.customer import (
    get_all_states_customer_statistics,
    get_customer_profile,
    get_state_customer_statistics,
)


@lru_cache
def get_customer_agent():
    return create_agent(
        name="Customer Agent",
        model=get_llm(),
        system_prompt=get_customer_prompt(),
        tools=[
            get_customer_profile,
            get_all_states_customer_statistics,
            get_state_customer_statistics,
        ],
    )


async def get_customer_details(query: str, config: RunnableConfig) -> str:
    """
    Get customer information using natural language.

    Use this when the user asks customer-related questions such as customer satisfaction,
    reviews, delivery status, support interactions, or order tracking. This tool takes a
    natural-language form question and replies in the natural language format to
    provide customer information.

    Input: Natural language question.
    Example: "What is the average customer satisfaction score for the last quarter?"
    """
    async with cl.Step(type="tool", name="get_customer_details") as step:
        result = await get_customer_agent().ainvoke(
            {"messages": [HumanMessage(content=query)]},
            config=config,
        )
        output = result["messages"][-1].text

        step.input = query
        step.output = output

        return output
