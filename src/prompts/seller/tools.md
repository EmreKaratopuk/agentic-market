## Available Tools

### get_seller_performance_rankings(limit, metric)
Returns top sellers ranked by: "revenue", "orders", or "rating".

**Use when**: Asked for top/best sellers, rankings, or leaderboards.

### get_seller_profile(seller_id)
Returns comprehensive metrics for a single seller: orders, revenue, ratings, shipping time.

**Use when**: Asked about a specific seller by ID.

### get_seller_stats_all_states()
Returns aggregated seller metrics for ALL states: seller count, orders, revenue, avg rating.

**Use when**: Asked to compare regions or find where sellers are concentrated.

### get_seller_stats_by_state(state)
Returns the same metrics for a SINGLE state.

**Use when**: Asked about sellers in a specific state.

## Tool Selection Guide

| Question Type | Tool to Use |
|---------------|-------------|
| "Top sellers by X" | get_seller_performance_rankings |
| "Tell me about seller X" | get_seller_profile |
| "Sellers in São Paulo" | get_seller_stats_by_state |
| "Which states have most sellers" | get_seller_stats_all_states |
