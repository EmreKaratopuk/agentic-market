"""Seller performance tools."""

from typing import Any, Literal

import chainlit as cl

from src.database import execute_query


@cl.step(type="tool", name="get_seller_performance_rankings")
async def get_seller_performance_rankings(
    limit: int = 10,
    metric: Literal["revenue", "orders", "rating"] = "revenue",
) -> dict[str, Any]:
    """
    Rank sellers by performance metrics.

    Aggregates order data to compute each seller's total orders, revenue,
    freight costs, average rating, and cancellation rate. Results are
    sorted by the specified metric.

    Args:
        limit: Maximum number of sellers to return. Defaults to 10.
        metric: Metric to sort by (revenue, orders, or rating). Defaults to "revenue".

    Returns:
        Dictionary with columns: seller_id, seller_city, seller_state,
        total_orders, total_revenue, total_freight, avg_rating, cancellation_rate.

    """
    query = """
    SELECT
        sellers.seller_id,
        sellers.seller_city,
        sellers.seller_state,
        COUNT(DISTINCT order_items.order_id)      AS total_orders,
        ROUND(SUM(order_items.price), 2)          AS total_revenue,
        ROUND(SUM(order_items.freight_value), 2)  AS total_freight,
        ROUND(AVG(order_reviews.review_score), 2) AS avg_rating,
        ROUND(
            AVG(CASE WHEN orders.order_status = 'canceled' THEN 100.0 ELSE 0 END), 2
        )                                         AS cancellation_rate
    FROM sellers
    INNER JOIN order_items
        ON sellers.seller_id = order_items.seller_id
    INNER JOIN orders
        ON order_items.order_id = orders.order_id
    LEFT JOIN order_reviews   -- Not every order has a review
        ON orders.order_id = order_reviews.order_id
    GROUP BY
        sellers.seller_id,
        sellers.seller_city,
        sellers.seller_state
    ORDER BY
        CASE ?
            WHEN 'revenue' THEN total_revenue
            WHEN 'orders' THEN total_orders
            WHEN 'rating' THEN avg_rating
        END DESC
    LIMIT ?
    """

    return await execute_query(query, [metric, limit])


@cl.step(type="tool", name="get_seller_profile")
async def get_seller_profile(seller_id: str) -> dict[str, Any]:
    """
    Retrieve comprehensive profile and metrics for a single seller.

    Computes lifetime statistics including order volume, product diversity,
    revenue, pricing, rating breakdown, activity timeline, and fulfillment
    performance.

    Args:
        seller_id: Seller ID to analyze.

    Returns:
        Dictionary with columns: seller_id, seller_city, seller_state,
        total_orders, unique_products, total_revenue, avg_item_price,
        avg_rating, five_star_reviews, negative_reviews, first_sale_at,
        last_sale_at, avg_shipping_time_days.

    """
    query = """
    SELECT
        sellers.seller_id,
        sellers.seller_city,
        sellers.seller_state,
        COUNT(DISTINCT order_items.order_id)                        AS total_orders,
        COUNT(DISTINCT order_items.product_id)                      AS unique_products,
        ROUND(SUM(order_items.price), 2)                            AS total_revenue,
        ROUND(AVG(order_items.price), 2)                            AS avg_item_price,
        ROUND(AVG(order_reviews.review_score), 2)                   AS avg_rating,
        COUNT(CASE WHEN order_reviews.review_score = 5 THEN 1 END)  AS five_star_reviews,
        COUNT(CASE WHEN order_reviews.review_score <= 2 THEN 1 END) AS negative_reviews,
        MIN(orders.order_purchase_timestamp)                        AS first_sale_at,
        MAX(orders.order_purchase_timestamp)                        AS last_sale_at,
        ROUND(AVG(
            JULIANDAY(orders.order_delivered_carrier_date)
            - JULIANDAY(orders.order_approved_at)
        ), 1)                                                       AS avg_shipping_time_days
    FROM sellers
    INNER JOIN order_items
        ON sellers.seller_id = order_items.seller_id
    INNER JOIN orders
        ON order_items.order_id = orders.order_id
    LEFT JOIN order_reviews   -- Not every order has a review
        ON orders.order_id = order_reviews.order_id
    WHERE sellers.seller_id = ?
    GROUP BY
        sellers.seller_id,
        sellers.seller_city,
        sellers.seller_state
    """

    return await execute_query(query, [seller_id])


@cl.step(type="tool", name="get_seller_stats_all_states")
async def get_seller_stats_all_states() -> dict[str, Any]:
    """
    Aggregate seller performance statistics for all states.

    Groups sellers by state and computes seller count, order volume,
    total revenue, average rating, and revenue efficiency per seller.

    Returns:
        Dictionary with columns: seller_state, seller_count, total_orders,
        total_revenue, avg_rating, revenue_per_seller. Sorted by total_revenue.

    """
    query = """
    SELECT
        sellers.seller_state,
        COUNT(DISTINCT sellers.seller_id)         AS seller_count,
        COUNT(DISTINCT order_items.order_id)      AS total_orders,
        ROUND(SUM(order_items.price), 2)          AS total_revenue,
        ROUND(AVG(order_reviews.review_score), 2) AS avg_rating,
        ROUND(
            SUM(order_items.price) / COUNT(DISTINCT sellers.seller_id), 2
        )                                         AS revenue_per_seller
    FROM sellers
    INNER JOIN order_items
        ON sellers.seller_id = order_items.seller_id
    INNER JOIN orders
        ON order_items.order_id = orders.order_id
    LEFT JOIN order_reviews
        ON orders.order_id = order_reviews.order_id
    GROUP BY
        sellers.seller_state
    ORDER BY total_revenue DESC
    """

    return await execute_query(query)


@cl.step(type="tool", name="get_seller_stats_by_state")
async def get_seller_stats_by_state(state: str) -> dict[str, Any]:
    """
    Aggregate seller performance statistics for a specific state.

    Groups sellers by state and computes seller count, order volume,
    total revenue, average rating, and revenue efficiency per seller.

    Args:
        state: State code to filter results (e.g., "SP", "RJ").

    Returns:
        Dictionary with columns: seller_state, seller_count, total_orders,
        total_revenue, avg_rating, revenue_per_seller.

    """
    query = """
    SELECT
        sellers.seller_state,
        COUNT(DISTINCT sellers.seller_id)         AS seller_count,
        COUNT(DISTINCT order_items.order_id)      AS total_orders,
        ROUND(SUM(order_items.price), 2)          AS total_revenue,
        ROUND(AVG(order_reviews.review_score), 2) AS avg_rating,
        ROUND(
            SUM(order_items.price) / COUNT(DISTINCT sellers.seller_id), 2
        )                                         AS revenue_per_seller
    FROM sellers
    INNER JOIN order_items
        ON sellers.seller_id = order_items.seller_id
    INNER JOIN orders
        ON order_items.order_id = orders.order_id
    LEFT JOIN order_reviews
        ON orders.order_id = order_reviews.order_id
    WHERE sellers.seller_state = ?
    GROUP BY
        sellers.seller_state
    ORDER BY total_revenue DESC
    """

    return await execute_query(query, [state])
