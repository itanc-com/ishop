# Registration API Specification

This document describes the API endpoint for user registration.

## Endpoint

`POST /api/v1/register`

## Request Body

```json
{
  "email": "user@example.com",
  "password": "string",
  "name": "string"
}
```

- `email` (string, required): The user's email address.
- `password` (string, required): The user's password.
- `name` (string, required): The user's full name.

## Response

### Success (201 Created)

```json
{
  "id": "user_id",
  "email": "user@example.com",
  "name": "string",
  "message": "Registration successful. Please verify your email."
}
```

### Error Responses

- **400 Bad Request**
  - Missing or invalid fields

    ```json
    {
      "error": "Email is required."
    }
    ```

- **409 Conflict**
  - Email already registered

    ```json
    {
      "error": "This email is already registered."
    }
    ```

## Email Verification

- After registration, the user will receive a verification email.
- A separate endpoint will handle email verification.

## Security Considerations

- Passwords must be hashed before storing.
- Rate limiting should be applied to prevent abuse.
- CAPTCHA may be required to avoid bots.

## Notes

- GDPR compliance must be ensured for user data.
- Additional user profile fields can be added in future releases.

## Related Endpoints

- [Login API Spec](./login.md)
- [Email Verification API Spec](./verify-email.md)
