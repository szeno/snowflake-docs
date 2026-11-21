# Nov 20, 2026: Postgres access roles for token authentication (*General availability*)

Postgres access roles for token authentication are now generally available. Enable a
Postgres access role for a Postgres user and grant it to Snowflake roles, application roles,
or users. Authorized callers can generate short-lived tokens to connect
as that Postgres user. Database and object privileges remain controlled by Postgres roles.

For more information, see
[Grant access with access roles](/user-guide/snowflake-postgres/postgres-authentication#label-sfpg-token-auth-access-roles) and
[GENERATE\_POSTGRES\_ACCESS\_TOKEN\_FOR\_USER](/sql-reference/functions/generate_postgres_access_token_for_user).
