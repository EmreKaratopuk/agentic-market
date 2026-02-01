## Examples

### Example 1: Specific Customer
User: "What can you tell me about customer abc123?"

Thought: Need to look up a specific customer profile.
Tool: get_customer_profile("abc123")

Response:
**Summary**: Customer Ab*** is a repeat buyer from São Paulo.

**Details**:
- Location: São Paulo, SP
- Total orders: 5
- Lifetime value: R$ 1,234.56
- Average rating given: 4.2
- Customer since: 2017-03-15

### Example 2: Regional Comparison
User: "Which states have the highest customer satisfaction?"

Thought: Need satisfaction data across all states to compare.
Tool: get_all_states_customer_statistics()

Response:
**Summary**: Northern states show the highest satisfaction scores.

**Details**:
| State | Satisfaction | Customers |
|-------|--------------|-----------|
| AM    | 4.5          | 234       |
| RR    | 4.4          | 89        |
| AP    | 4.3          | 67        |

**Insights**: Smaller customer bases in these states may contribute to higher scores.
