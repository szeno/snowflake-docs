# Specify Snowflake context with Snowflake REST APIs

You can specify aspects of Snowflake context when making a request to the Snowflake REST APIs.

Using request headers, you can specify the following in the context of a REST API call:

- The Snowflake role used to authorize the request with the `X-Snowflake-Role` header.
- The Snowflake warehouse used to execute the request with the `X-Snowflake-Warehouse` header.

Instead of relying on a user’s default settings, these headers make each call explicit, isolated, and auditable. You guarantee that
each request uses the correct role and warehouse without needing extra API calls to set context.

By specifying context when making REST API requests, you can accomplish the following tasks:

- Run stateless calls.

  Guarantee that a call uses a specific role without needing a separate API call first to set the session context.
- Avoid mutating users.

  Safely switch roles per-request instead of running ALTER USER … SET DEFAULT\_ROLE=…, which is slow and affects all other sessions for
  that user.
- Enable on-demand compute.

  Allow users or service accounts without a default warehouse to run queries or create procedures by simply providing the
  `X-Snowflake-Warehouse` header.
- Simplify user management.

  Use one service user granted multiple roles—for example, READER and WRITER. Your application then sends the `X-Snowflake-Role`
  header to pick the right permission for the right task. In this way, you can avoid managing multiple single-role users.

## Precedence

When a header is provided, it takes precedence over a user’s default settings, in the following order:

1. Headers (if provided) are used.
2. Otherwise, the session’s default role or default warehouse is used.
3. If neither is available where required, the call fails.

## Specify the role to use when authorizing the request

You can specify the role to use when authorizing the request by using the `X-Snowflake-Role` header.

### Requirements

- The role you specify must exist, be granted to the user, and be allowed by the authentication method in use.
- If you use a [programmatic access token (PAT)](/developer-guide/snowflake-rest-api/authentication#label-sfrest-authenticating-pat), the requested role must be within the PAT’s
  `ROLE_RESTRICTION`. If you specify a more privileged role than the PAT allows, the request will fail even if the user was granted
  the specified role.

### Example

The following example creates a database by using the ACCOUNTADMIN role for authorization regardless of the user’s default role.

You can specify the `X-Snowflake-Role` header’s value either in double quotes or without quotes.

Copy code

```
curl -X POST "$API_BASE/database/databases" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Snowflake-Role: ACCOUNTADMIN" \
  -d '{"name": "HDR_DEMO_DB", "comment": "Created via REST with role header"}'
```

## Specify the warehouse on which a statement should execute

You can specify the warehouse to use when executing statements by using the `X-Snowflake-Warehouse` header. Such statements include
those executing procedures, creating Python functions, and executing queries that need compute resources.

### Requirements

- The role in effect must have the USAGE privilege on the warehouse.
- If no default warehouse is set and this header is omitted, warehouse-dependent calls will fail.

### Example

The following example creates a Python procedure that uses the `BUILD_WH` warehouse. The specified role must have the USAGE privilege
on the warehouse. The `PYTHON_WH_TEST` procedure created returns the active warehouse name.

You can specify the `X-Snowflake-Warehouse` header’s value either in double quotes or without quotes.

Copy code

```
curl -X POST "$API_BASE/procedure/databases/TEST_DB/schemas/TEST_SCHEMA/procedures" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Snowflake-Role: ACCOUNTADMIN" \
  -H "X-Snowflake-Warehouse: BUILD_WH" \
  -d '{
        "name": "PYTHON_WH_TEST",
        "arguments": [],
        "return_type": {"datatype": "VARIANT", "nullable": true},
        "language_config": {
          "python_function": {
            "handler":"main",
            "runtime_version":"3.11",
            "packages":["snowflake-snowpark-python"]
          }
        },
        "body": "def main(session):\n    return {\"warehouse\": session.get_current_warehouse()}"
      }'
```
