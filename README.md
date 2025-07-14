# Guidance for Task: Secure Profile Access with Token Authentication and Async Access Logging

## Task Requirements
- Implement a FastAPI backend providing two endpoints: `/login` (for obtaining a JWT token) and `/profile` (to fetch user profile data).
- The `/login` endpoint uses a mock user and returns a valid JWT for use with the Bearer token flow.
- The `/profile` route **must** be protected via OAuth2 Bearer authentication, only allowing access with a valid JWT.
- Use **Pydantic models** for request validation and response formats on both routes.
- Ensure all accesses of `/profile` are asynchronously logged into an in-memory list, including the user and timestamp. Use FastAPI's BackgroundTasks.
- Implement **structured error responses** for common authentication/authorization errors.
- Organize endpoints using FastAPI routers to support modular, testable code.
- Do **not** use any database or persistent storage; all logs and users are in-memory.

## Expectations
- Correctly complete any partial implementation and fill in any missing pieces.
- Make sure JWT creation, validation, and expiration are correctly handled.
- Ensure the async access logging is non-blocking and performed for each `/profile` call.
- Maintain clarity and organization—keep code production-like and easy to test/extend.

## Verifying Your Solution
- You should be able to authenticate with `/login` (with mock credentials), retrieve and use the token, then access `/profile`.
- Attempting to access `/profile` without a valid token should return an appropriate error structure.
- The profile access log should accurately record each access asynchronously, including who accessed and when.
- Error responses should be consistent with the provided Pydantic error model.
- Code organization should be modular and follow good FastAPI conventions.
