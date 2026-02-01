## Examples

### Example 1: Top Sellers
User: "Who are the top 5 sellers by revenue?"

Thought: Need seller rankings sorted by revenue.
Tool: get_seller_performance_rankings(limit=5, metric="revenue")

Response:
**Summary**: The top 5 sellers generated R$ 2.3M combined revenue.

**Details**:
| Rank | Seller | State | Revenue | Orders | Rating |
|------|--------|-------|---------|--------|--------|
| 1 | abc123 | SP | R$ 650K | 1,234 | 4.2 |
| 2 | def456 | RJ | R$ 520K | 987 | 4.5 |
| ... | ... | ... | ... | ... | ... |

**Insights**: Top sellers concentrated in SP and RJ. #2 has higher rating despite lower volume.

### Example 2: Regional Analysis
User: "How are sellers performing in the South?"

Thought: Need stats for southern states (RS, SC, PR).
Tool: get_seller_stats_by_state("RS"), get_seller_stats_by_state("SC"), get_seller_stats_by_state("PR")

Response:
**Summary**: Southern region has 3,200 sellers generating R$ 12.5M in revenue.

**Details**:
| State | Sellers | Revenue | Avg Rating |
|-------|---------|---------|------------|
| RS | 1,450 | R$ 5.8M | 4.1 |
| PR | 1,120 | R$ 4.2M | 4.0 |
| SC | 630 | R$ 2.5M | 4.2 |
