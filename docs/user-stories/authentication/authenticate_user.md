# User Story 002: Authenticate as an Existing User

**As a** registered user
**I want** to log in using my email and password
**So that** I can securely access my account and personalized features

## Acceptance Criteria
- [x] Login form includes email and password fields
- [x] Form validates input and provides helpful error messages for invalid credentials
- [x] Upon successful authentication, user receives an access token
- [x] Invalid login attempts are logged and handled securely
- [ ] User is redirected to their dashboard after login

## Notes
- Passwords are verified securely using a password context
- Error messages do not reveal whether the email or password was incorrect
- Consider rate limiting and account lockout for repeated failed attempts

## Related Links
- [Register as a New User](register_new_user.md)
