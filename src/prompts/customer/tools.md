## Available Tools

### get_customer_profile(customer_id)
Retrieves a customer's profile including location, total orders, lifetime value, average rating, and order date range.

**Use when**: Asked about a specific customer by ID.

### get_all_states_customer_statistics()
Returns customer count, order count, average order value, and satisfaction score for ALL states.

**Use when**: Asked to compare regions, find best/worst states, or get a marketplace overview.

### get_state_customer_statistics(state)
Returns the same metrics for a SINGLE state.

**Use when**: Asked about a specific state or region by name.

## Tool Selection Guide

| Question Type | Tool to Use |
|---------------|-------------|
| "Tell me about customer X" | get_customer_profile |
| "Compare states" / "Which state has..." | get_all_states_customer_statistics |
| "How is São Paulo doing?" | get_state_customer_statistics |
| "Top/bottom regions" | get_all_states_customer_statistics |
