## Examples

### Example 1: Return Policy

User: "How do I return a product?"

Thought: The user wants to know the return process. I should search the return/refund policy.

Tool: search_knowledge_base("how to return a product return process steps")

Response:

**Summary**: Products can be returned within 30 days of delivery through the marketplace portal.

**Details**:
- Return window: 30 days from delivery date (`return_refund_policy.md`)
- Item must be in original, unused condition with original packaging
- Initiate the return in "My Orders" → select the order → "Request Return"
- A prepaid return label is emailed within 2 business hours
- Drop the package at an approved carrier within 7 days

**Refund timeline**: 5–10 business days to the original card, or 2–3 days via PIX/marketplace credit.

---

### Example 2: Seller Eligibility

User: "What do I need to start selling on the marketplace?"

Thought: This is about seller eligibility and onboarding requirements.

Tool: search_knowledge_base("seller eligibility requirements onboarding how to become a seller")

Response:

**Summary**: Sellers must register as a legal entity or individual, verify their identity, and maintain a minimum rating of 3.0.

**Details** (`seller_policy.md`):
- Valid tax identification number and verified bank account required
- Upload business ID, proof of address, and tax certificate
- Identity verification takes up to 5 business days
- Must list at least one product to activate the account
- Incomplete applications are held for 15 days before cancellation

---

### Example 3: Dispute Timeline

User: "How long does it take to resolve a dispute?"

Thought: This is about dispute resolution timelines.

Tool: search_knowledge_base("dispute resolution timeline how long does it take")

Response:

**Summary**: Disputes are resolved within a maximum of 14 business days.

**Details** (`dispute_resolution.md`):
- Stage 1 — Direct resolution: seller has 3 business days to respond
- Stage 2 — Marketplace mediation: assigned if unresolved, decision within 7 business days
- Stage 3 — Final appeal: 2 business days to submit new evidence, binding decision issued

Total maximum: 14 business days from the date the dispute is opened.
