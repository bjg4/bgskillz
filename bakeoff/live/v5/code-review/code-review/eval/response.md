## Critical
- `login`: SQL built with f-string from `user` and `pwd` — **SQL injection**. Use parameterized query: `cursor.execute("SELECT * FROM users WHERE name = %s AND pass = %s", (user, pwd))`.

## Major
- Passwords in SQL imply plaintext storage — hash with bcrypt/argon2 and compare in app code.

## Minor
- Add rate limiting on failed login attempts.
