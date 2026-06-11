## Plan stress-test: real-time chat at 10M users

I'll walk through several areas — answer what you can, then we'll go deeper.

### Requirements
- What is "real-time" for you — sub-100ms delivery, or eventual seconds?
- Is 10M **concurrent** connections or registered users with lower peak online?

### Architecture (recommended direction)
- At true chat scale you likely need **WebSockets or SSE** fronted by a connection layer, not polling.
- **Recommended:** partition users into rooms/channels; avoid single global fan-out.

### Security
- How will you authenticate connections and authorize room membership?

### Operations
- What's your target for message durability vs latency — full persistence or ephemeral?

**Recommended next step:** nail down concurrent connection peak (not total registered users) — that number drives sharding, Redis/pub-sub vs dedicated message bus, and cost.

Which of the requirement questions above is hardest for you to answer right now?
