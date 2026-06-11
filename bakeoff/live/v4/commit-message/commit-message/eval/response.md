```
feat(auth): add JWT login endpoint

Introduce POST /login that validates credentials and returns signed JWT access tokens.
Uses existing user store; tokens expire after 24h.
```

Subject is imperative, under 72 characters, and describes the capability added rather than a vague "update code."
