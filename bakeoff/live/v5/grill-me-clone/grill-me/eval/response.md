Before we design components: **what peak concurrent connections do you need to support** — not total registered users, but simultaneous online users sending messages?

**Recommended answer:** For "10M users" products, concurrent peaks are often 1–5% of registered (50k–500k). That number determines whether you need a dedicated connection tier (WebSockets + sticky routing) vs a simpler pub/sub backbone. If you don't know yet, instrument early and cap MVP to one region first.

Your turn — what's your best estimate for peak concurrent connections?
