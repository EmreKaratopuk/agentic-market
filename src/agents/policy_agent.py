from functools import lru_cache

import chainlit as cl
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from src.llm import get_llm
from src.prompts import get_policy_prompt
from src.tools.search import search_knowledge_base


@lru_cache
def get_policy_agent():
    return create_agent(
        name="Policy Agent",
        model=get_llm(),
        system_prompt=get_policy_prompt(),
        tools=[search_knowledge_base],
    )


async def get_policy_details(query: str, config: RunnableConfig) -> str:
    """
    Get marketplace policy and FAQ information using natural language.

    Use this when the user asks about marketplace policies, rules, procedures,
    seller requirements, buyer rights, shipping SLAs, return and refund policies,
    dispute resolution, or how any marketplace process works. This tool takes a
    natural-language question and replies with information retrieved from official
    policy documents.

    Input: Natural language question.
    Example: "What is the return window for products?"
    Example: "What are the rules for selling on the marketplace?"
    Example: "How long does dispute resolution take?"
    Example: "What shipping SLA applies to the Northeast region?"
    """
    async with cl.Step(type="tool", name="get_policy_details") as step:
        result = await get_policy_agent().ainvoke(
            {"messages": [HumanMessage(content=query)]},
            config=config,
        )
        output = result["messages"][-1].text

        step.input = query
        step.output = output

        return output
