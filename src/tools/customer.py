"""Customer intelligence tools."""

from typing import Any

import chainlit as cl

from src.database import execute_query


@cl.step(type="tool", name="get_customer_profile")
async def get_customer_profile(customer_id: str) -> dict[str, Any]:
    """
    Retrieve a customer's profile with purchase history summary.

    Fetches redacted customer name (format: "AB***"), location, order statistics,
    lifetime spend, average review rating, and date range of orders.

    Args:
        customer_id: Customer ID or customer unique ID to look up.

    Returns:
        Customer profile including redacted name, city, state, total orders,
        lifetime value, average rating, first order date, and last order date.

    """
    query = """
    SELECT
        customers.customer_unique_id,
        SUBSTR(customers.customer_name, 1, 2) || '***' AS customer_name,
        customers.customer_city,
        customers.customer_state,
        COUNT(DISTINCT orders.order_id)                AS total_orders,
        ROUND(SUM(order_payments.payment_value), 2)    AS lifetime_spend,
        ROUND(AVG(order_reviews.review_score), 2)      AS avg_rating,
        MAX(orders.order_purchase_timestamp)           AS last_order_at,
        MIN(orders.order_purchase_timestamp)           AS first_order_at
    FROM customers
    INNER JOIN orders
        ON customers.customer_id = orders.customer_id
    INNER JOIN order_payments
        ON orders.order_id = order_payments.order_id
    LEFT JOIN order_reviews  -- Not every order has a review
        ON orders.order_id = order_reviews.order_id 
    WHERE customers.customer_id = ?
        OR customers.customer_unique_id = ?
    GROUP BY
        customers.customer_unique_id,
        customers.customer_name,
        customers.customer_city,
        customers.customer_state
    """

    return await execute_query(query, [customer_id, customer_id])


@cl.step(type="tool", name="get_all_states_customer_statistics")
async def get_all_states_customer_statistics() -> dict[str, Any]:
    """
    Retrieve customer and order statistics for all states.

    Returns metrics including customer count, order count, average order value,
    and average satisfaction score (review score, 1-5 scale) for each state.

    Returns:
        State-level statistics sorted by customer count in descending order.

    """
    query = """
    SELECT
        customers.customer_state,
        COUNT(DISTINCT customers.customer_unique_id) AS customer_count,
        COUNT(DISTINCT orders.order_id)              AS order_count,
        ROUND(AVG(order_payments.payment_value), 2)  AS avg_order_value,
        ROUND(AVG(order_reviews.review_score), 2)    AS avg_satisfaction
    FROM customers
    INNER JOIN orders
        ON customers.customer_id = orders.customer_id
    INNER JOIN order_payments
        ON orders.order_id = order_payments.order_id
    LEFT JOIN order_reviews   -- Not every order has a review
        ON orders.order_id = order_reviews.order_id
    GROUP BY
        customers.customer_state
    ORDER BY
        customer_count DESC
    """
    return await execute_query(query)


@cl.step(type="tool", name="get_state_customer_statistics")
async def get_state_customer_statistics(state: str) -> dict[str, Any]:
    """
    Retrieve customer and order statistics for a specific state.

    Returns metrics including customer count, order count, average order value,
    and average satisfaction score.

    Args:
        state: State code to filter results (e.g., "SP", "RJ").

    Returns:
        Statistics for the specified state.

    """
    query = """
    SELECT
        customers.customer_state,
        COUNT(DISTINCT customers.customer_unique_id) AS customer_count,
        COUNT(DISTINCT orders.order_id)              AS order_count,
        ROUND(AVG(order_payments.payment_value), 2)  AS avg_order_value,
        ROUND(AVG(order_reviews.review_score), 2)    AS avg_satisfaction
    FROM customers
    INNER JOIN orders
        ON customers.customer_id = orders.customer_id
    INNER JOIN order_payments
        ON orders.order_id = order_payments.order_id
    LEFT JOIN order_reviews  -- Not every order has a review
        ON orders.order_id = order_reviews.order_id
    WHERE customers.customer_state = ?
    GROUP BY
        customers.customer_state
    ORDER BY
        customer_count DESC
    """
    return await execute_query(query, [state])
