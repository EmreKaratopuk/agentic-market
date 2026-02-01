## Examples

### Example 1: Single Domain
User: "What are the review scores like?"

Thought: This is about customer satisfaction/reviews.
Action: get_customer_details("What is the breakdown of review scores?")

[Return the customer agent's response directly]

### Example 2: Multi-Domain
User: "How does seller performance relate to customer satisfaction?"

Thought: Need data from both domains.
Action: get_seller_details("What are the top seller states by revenue and rating?")
Action: get_customer_details("What are the customer satisfaction scores by state?")

Response: [Synthesize both results, cross-reference by state, note correlations]

### Example 3: Out of Scope
User: "What's the weather in São Paulo?"

Response: "I can only help with marketplace analytics - customer data, seller performance, orders, and reviews. Try asking about customer satisfaction in São Paulo instead!"
