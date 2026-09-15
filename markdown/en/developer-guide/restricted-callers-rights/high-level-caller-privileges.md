# High-level caller privileges

In addition to fine-grained caller grants, an administrator can grant a small set of *high-level caller privileges*. Each
high-level caller privilege authorizes a broad category of operations (for example, all read operations in a database) without the
need to enumerate every individual caller grant.

Note

High-level caller privileges on an account apply to all objects in the account.

The following high-level caller privileges can be granted with a [GRANT CALLER](/sql-reference/sql/grant-caller) statement.

| High-level caller privilege | Can be granted on | Description |
| --- | --- | --- |
| DATA READ | Account, database, schema | Read data from objects in the target container. |
| DATA WRITE | Account, database, schema | Write data to objects in the target container. |
| OBJECT DISCOVERY | Account, database, schema | Discover objects in the target container (for example, using SHOW) without reading their data. |
| COMPUTE USAGE | Account | Use compute resources in the account. |
| PROGRAM USAGE | Account, database, schema | Invoke certain executables in the target container. |
| GRANT MANAGEMENT | Account, database, schema | Run GRANT and REVOKE statements for permissions on in-account objects, and create [references](/sql-reference/references) to those objects. |
| OBJECT MANAGEMENT | Account, database, schema | Take full control of non-sensitive objects in the target container. |
| FULL MANAGEMENT | Account | All operations permitted in the account. |

Expand

Show lessSee more

Note

High-level caller privileges can only be granted as caller grants. They cannot be granted as regular privileges (for example,
`GRANT DATA WRITE ON ACCOUNT TO ROLE r` isn’t allowed).

Granting `ALL [INHERITED] CALLER PRIVILEGES` on an object doesn’t include high-level caller privileges. Granting
`CALLER OWNERSHIP` on an object doesn’t imply any high-level caller privilege.

Caution

Granting FULL MANAGEMENT, or any high-level caller privilege at the account level, significantly broadens what an RCR
executable can do on behalf of the caller. If a highly privileged role such as ACCOUNTADMIN runs the executable, the
executable can perform the corresponding sensitive operations within that role’s permissions. Grant the smallest high-level
caller privilege that lets the executable do its job, and grant it at the narrowest container (schema, then database, then
account).

## Privilege relationship

Some high-level privileges can naturally overlap. For example, DATA READ, DATA WRITE, OBJECT MANAGEMENT, and OBJECT DISCOVERY
can each authorize discovering a table, but only DATA READ authorizes reading the table’s data. One high-level privilege can
also subsume another one. For example, OBJECT MANAGEMENT subsumes OBJECT DISCOVERY and COMPUTE USAGE.

## DATA READ

The DATA READ high-level caller privilege authorizes an RCR executable to read data from objects in the target container.
This currently includes tables, views, Cortex Search Services, streams, stages, and workspaces.

DATA READ doesn’t authorize any of the following:

- Writing or modifying data.
- Creating or altering objects.
- Running GRANT or REVOKE statements.
- Invoking executables.

DATA READ can be granted on an account, database, or schema.

The following example lets all RCR executables owned by `rpt_owner` read data in the `reporting` database:

Copy code

```
GRANT CALLER DATA READ ON DATABASE reporting TO ROLE rpt_owner;
```

## DATA WRITE

The DATA WRITE high-level caller privilege authorizes an RCR executable to write data to objects in the target container. This currently includes tables only.

UPDATE and DELETE operations require the ability to read existing data, and can’t be authorized by DATA WRITE alone. DATA READ
may be used in conjunction to support these operations.

DATA WRITE doesn’t authorize any of the following:

- Reading data.
- Creating or altering objects.
- Running GRANT or REVOKE statements.
- Invoking executables.

DATA WRITE can be granted on an account, database, or schema.

The following example lets all RCR executables owned by `etl_owner` read from any schema in the `raw` database and write to
tables in the `curated.silver` schema:

Copy code

```
GRANT CALLER DATA READ  ON DATABASE raw            TO ROLE etl_owner;
GRANT CALLER DATA WRITE ON SCHEMA   curated.silver TO ROLE etl_owner;
```

## OBJECT DISCOVERY

The OBJECT DISCOVERY high-level caller privilege authorizes an RCR executable to discover objects in the target container —
that is, to see that an object exists — without reading the object’s data. This currently includes operations such as
SHOW on objects in the container.

OBJECT DISCOVERY doesn’t authorize any of the following:

- Reading or writing data.
- Creating or altering objects.
- Running GRANT or REVOKE statements.
- Invoking executables.

OBJECT DISCOVERY can be granted on an account, database, or schema.

## COMPUTE USAGE

The COMPUTE USAGE high-level caller privilege authorizes an RCR executable to use compute resources. This currently includes
warehouses and compute pools.

COMPUTE USAGE can only be granted on an account.

## PROGRAM USAGE

The PROGRAM USAGE high-level caller privilege authorizes an RCR executable to invoke certain executables in the target
container. This currently includes:

- User-defined functions (UDFs) and user-defined table functions (UDTFs).
- Stored procedures.
- Streamlit in Snowflake apps.
- Snowpark Container Services.
- Cortex Agents.
- MCP servers.

PROGRAM USAGE can be granted on an account, database, or schema.

## GRANT MANAGEMENT

The GRANT MANAGEMENT high-level caller privilege authorizes an RCR executable to do the following on in-account objects in the
target container:

- Run GRANT and REVOKE statements for permissions.
- Create transient and persistent [references](/sql-reference/references).
  - The reference’s privileges and object must be covered by caller grants.

The following sensitive grants aren’t covered by GRANT MANAGEMENT and require FULL MANAGEMENT instead:

- Grants on accounts and account roles
- Grants to shares and shared database roles
- Ownership transfer of executables
- Caller grants

GRANT MANAGEMENT can be granted on an account, database, or schema.

The following example shows the caller grants that allow an RCR executable owned by `data_owner` to create a SELECT reference,
but not an INSERT reference, on a table in the `data` schema:

Copy code

```
GRANT CALLER DATA READ        ON SCHEMA data TO ROLE data_owner;
GRANT CALLER GRANT MANAGEMENT ON SCHEMA data TO ROLE data_owner;

-- Allowed:
SELECT SYSTEM$REFERENCE('TABLE', 'data.raw', 'PERSISTENT', 'SELECT');

-- Blocked: no CALLER DATA WRITE grant.
SELECT SYSTEM$REFERENCE('TABLE', 'data.raw', 'PERSISTENT', 'INSERT');
```

## OBJECT MANAGEMENT

The OBJECT MANAGEMENT high-level caller privilege authorizes an RCR executable to take full control of non-sensitive objects in
the target container.

With exceptions (see below), OBJECT MANAGEMENT allows:

- All operations on all objects inside accounts (but not including accounts themselves), except the data-access operations
  covered by DATA READ and DATA WRITE.
- Creation of objects inside accounts.

OBJECT MANAGEMENT doesn’t cover the following sensitive operations. They require FULL MANAGEMENT instead:

- Alteration of the account.
- Creation or alteration of integrations, listings, shares, and users.
- Creation of executables (including, but not limited to, procedures, UDFs, UDTFs, tasks, alerts, Streamlit in Snowflake apps,
  services, service classes, agents, MCP servers, dbt projects, DCM projects, notebooks, and notebook projects).
- Invocation of executables not covered by PROGRAM USAGE.
- Execution of a job service.
- Creation of a [programmatic access token](/user-guide/programmatic-access-tokens) (PAT).
- Alteration of the `EXECUTE AS` property of executables.
- Writing to stages, repositories, and workspaces.

OBJECT MANAGEMENT can be granted on an account, database, or schema.

The following example lets a Snowflake Native App read and write data in its database, and also provision and grant access to
objects in that database:

Copy code

```
GRANT CALLER DATA READ         ON DATABASE my_app_db TO APPLICATION my_app;
GRANT CALLER DATA WRITE        ON DATABASE my_app_db TO APPLICATION my_app;
GRANT CALLER OBJECT MANAGEMENT ON DATABASE my_app_db TO APPLICATION my_app;
GRANT CALLER GRANT MANAGEMENT  ON DATABASE my_app_db TO APPLICATION my_app;
```

## FULL MANAGEMENT

The FULL MANAGEMENT high-level caller privilege authorizes an RCR executable to perform every operation in the account.

FULL MANAGEMENT can only be granted on an account.

## Operations and the required high-level caller privilege

The following operations were previously blocked inside an RCR executable and are now allowed only when the executable owner
holds at least the high-level caller privilege shown. These operations may be authorized by regular permissions, but they aren’t
authorized by the corresponding caller permissions. For example, `CALLER CREATE PROCEDURE ON SCHEMA` doesn’t allow the creation
of a procedure. Only `CALLER FULL MANAGEMENT` does.

| Operation | Minimum high-level caller privilege | Notes |
| --- | --- | --- |
| Create a transient or persistent [reference](/sql-reference/references). | GRANT MANAGEMENT | The reference’s privileges and object must be covered by caller grants. |
| Run GRANT or REVOKE statements on in-account objects. | GRANT MANAGEMENT | Except for sensitive grants. |
| Run GRANT or REVOKE statements for sensitive grants. | FULL MANAGEMENT |  |
| Create an [external stage](/sql-reference/sql/create-stage) without a storage integration, COPY INTO an external URL without a storage integration, or COPY INTO a table from an external URL without a storage integration. | FULL MANAGEMENT | The same operations that use a storage integration don’t require FULL MANAGEMENT. |
| Set certain sensitive session parameters with ALTER SESSION SET (for example, `S3_STAGE_VPCE_DNS_NAME`). Other session parameters may also require FULL MANAGEMENT. | FULL MANAGEMENT | Most session parameters don’t require a high-level caller privilege. |
| Create or transfer ownership of an executable. | FULL MANAGEMENT |  |
| Alter the execution mode of an executable (for example, `ALTER PROCEDURE ... EXECUTE AS OWNER`). | FULL MANAGEMENT |  |
| Create a [programmatic access token](/user-guide/programmatic-access-tokens) (PAT). | FULL MANAGEMENT |  |
| Execute a Job Service, dbt project, DCM project, notebook, or notebook project. | FULL MANAGEMENT | Execution of these entities doesn’t propagate RCR semantics, so it’s guarded at the highest level. |
| Inspect query results from outside the current RCR invocation, for example through [LAST\_QUERY\_ID](/sql-reference/functions/last_query_id), [RESULT\_SCAN](/sql-reference/functions/result_scan), or [DESC RESULT](/sql-reference/sql/desc-result). | FULL MANAGEMENT | Inspecting query results that originated *inside* the current RCR invocation doesn’t require any caller privileges. |

Expand

Show lessSee more

Note

All operations that were previously blocked in RCR have now been unblocked.

## Adding new privileges to a high-level caller privilege

When Snowflake introduces a new privilege or object type, it might be added to an existing high-level caller privilege. This
expands the set of operations that an existing grant authorizes. Snowflake documents the *intent* of each high-level caller
privilege rather than an exhaustive list of covered operations, and adding new members is generally not treated as a behavior
change release (BCR).

When granting a high-level caller privilege, reason about the operations you want to authorize in terms of the description of
the privilege, not a fixed permission list.
