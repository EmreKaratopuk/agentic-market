from functools import lru_cache

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from src.agents.customer_agent import get_customer_details
from src.agents.seller_agent import get_seller_details
from src.llm import get_llm
from src.prompts import get_supervisor_prompt


@lru_cache
def get_supervisor_agent():
    return create_agent(
        name="Supervisor Agent",
        model=get_llm(),
        system_prompt=get_supervisor_prompt(),
        tools=[get_seller_details, get_customer_details],
        checkpointer=InMemorySaver(),
    )
