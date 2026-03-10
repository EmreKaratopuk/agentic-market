import chainlit as cl
from chainlit.cli import run_chainlit
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from src.agents.supervisor_agent import get_supervisor_agent
from src.database import get_database
from src.vectorstore import get_vectorstore
from src.guardrails import input_guard


@cl.set_starters
async def set_starters(user: cl.User | None):
    return [
        cl.Starter(
            label="Top Sellers",
            message="Who are the top 5 sellers by revenue?",
        ),
        cl.Starter(
            label="Regional Customer Stats",
            message="Show me customer statistics for all states.",
        ),
        cl.Starter(
            label="Best Rated Sellers",
            message="Which sellers have the highest customer ratings?",
        ),
        cl.Starter(
            label="Seller Requirements",
            message="What are the requirements to start selling on the marketplace?",
        ),
    ]


@cl.on_chat_start
async def on_start():
    """Initialize the agent when a new chat session starts."""
    graph = get_supervisor_agent()
    cl.user_session.set("graph", graph)


@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming user messages."""
    _sanitized, is_valid, _risk = input_guard.scan(message.content)
    if not is_valid:
        await cl.Message(
            content="I can only help with marketplace analytics questions.\nTry asking about customers, sellers, or orders.",
        ).send()
        return

    graph = cl.user_session.get("graph")
    if graph is None:
        await cl.Message(content="Session not initialized. Please refresh.").send()
        return

    config = RunnableConfig(
        configurable={"thread_id": cl.context.session.id},
        recursion_limit=5,
    )

    llm_output = None

    message_content = str(message.content)
    async for event in graph.astream_events(
        {"messages": [HumanMessage(content=message_content)]},
        config=config,
    ):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"]

            if hasattr(chunk, "tool_call_chunks") and chunk.tool_call_chunks:
                continue

            if hasattr(chunk, "content") and chunk.content:
                content = chunk.content
                if isinstance(content, list):
                    content = "".join(
                        block.get("text", "") if isinstance(block, dict) else str(block)
                        for block in content
                    )
                if content:
                    if llm_output is None:
                        llm_output = cl.Message(content="")
                        await llm_output.send()
                    await llm_output.stream_token(content)

    if llm_output:
        await llm_output.update()


def main():
    load_dotenv()
    get_database()
    get_vectorstore()

    run_chainlit(__file__)


if __name__ == "__main__":
    main()
