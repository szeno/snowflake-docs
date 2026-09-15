# Manage users

The Snowflake REST [User API](/developer-guide/snowflake-rest-api/reference/user.html) provides the following endpoints to manage Snowflake users:

**Snowflake REST User API endpoints**

| Endpoint | Description |
| --- | --- |
| `POST /api/v2/users` | Creates a Snowflake user. |
| `GET /api/v2/users` | Lists the users in the system. |
| `GET /api/v2/users/{name}` | Fetches user information using the result of the DESCRIBE command. |
| `DELETE /api/v2/users/{name}` | Deletes a user with the given name. |
| `PUT /api/v2/users/{name}` | Creates a new, or alters an existing, user. |
| `GET /api/v2/users/{name}/grants` | List all grants to the user. |
| `POST /api/v2/users/{name}/grants` | Grants a role to the specified user. |
| `POST /api/v2/users/{name}/grants:revoke` | Revokes grants from the specified user. |

Expand

Show lessSee more

For reference documentation, see [Snowflake User API reference](/developer-guide/snowflake-rest-api/reference/user.html)
