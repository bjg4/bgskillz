## Critical

- **Line 2–3: SQL injection via string interpolation** — The query builds SQL with f-string interpolation from `user` and `pwd`. An attacker can inject SQL through either parameter. **Fix:** use parameterized queries (`cursor.execute("SELECT ... WHERE name=? AND pass=?", (user, pwd))`) or an ORM with bound parameters.

## Major

- **Password handling** — Plaintext password comparison in SQL suggests passwords may be stored unsafely. Verify hashing (bcrypt/argon2) and compare hashes in application code, not SQL.

## Minor

- Function name `login` is clear; consider rate limiting and logging failed attempts at the service layer.
