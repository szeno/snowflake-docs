# SHOW APPLICATION SERVICES

Lists the
[Application Services](/sql-reference/sql/create-application-service)
for which you have access privileges.

See also:
:   [CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service) ,
    [ALTER APPLICATION SERVICE](/sql-reference/sql/alter-application-service) ,
    [DESCRIBE APPLICATION SERVICE](/sql-reference/sql/desc-application-service) ,
    [DROP APPLICATION SERVICE](/sql-reference/sql/drop-application-service)

## Syntax

Copy code

```
SHOW APPLICATION SERVICES
  [ LIKE '<pattern>' ]
  [ IN { ACCOUNT | DATABASE [ <database_name> ] | SCHEMA [ <schema_name> ] } ]
  [ LIMIT <rows> ]
```

## Parameters

`LIKE 'pattern'`
:   Filters the output by name.

`IN { ACCOUNT | DATABASE [ database_name ] | SCHEMA [ schema_name ] }`
:   Scopes the listing to an account, database, or schema.

`LIMIT rows`
:   Limits the maximum number of rows returned.

## Access control requirements

You can see a service in the output if you have at least one privilege on it,
or if you own it.

## Output

The command returns one row per service with the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the service was created. |
| `name` | Name of the service. |
| `status` | Current lifecycle state of the underlying managed service. One of `PENDING`, `RUNNING`, `FAILED`, `DONE`, `SUSPENDING`, `SUSPENDED`, `CANCELLED`, `DELETING`, `DELETED`, or `INTERNAL_ERROR`. |
| `database_name` | Database that contains the service. |
| `schema_name` | Schema that contains the service. |
| `query_warehouse` | Warehouse used by the service when a container connects to Snowflake without specifying a warehouse. |
| `compute_pool` | Empty when the service uses Snowflake-managed compute. |
| `url` | Public endpoint URL for the service, if any. |
| `privatelink_url` | PrivateLink endpoint URL for the service, if any. |
| `owner` | Role that owns the service. |
| `owner_role_type` | Type of the owning role, such as `ROLE`. |
| `created_by` | Name of the user who created the service. |
| `source` | JSON object describing the deployed package, with keys `artifactRepository`, `package`, `version`, and `alias`. |
| `resumed_on` | Date and time when the service was most recently resumed. |
| `suspended_on` | Date and time when the service was most recently suspended. |
| `is_upgrading` | `TRUE` when an upgrade is in progress. |
| `auto_resume` | Whether auto-resume is enabled. |
| `auto_suspend_secs` | Configured auto-suspend timeout in seconds. `0` means auto-suspend is disabled. |
| `external_access_integrations` | External access integrations attached to the service. |
| `comment` | Service comment, if any. |
| `additional_properties` | JSON object of additional presentation metadata from your optional `app.yml` manifest (for example, `label` and `description` from the `profile` section of [app.yml manifest for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/app-yml)). |
| `execute_as_role` | For a service in a personal database, the role that owner’s rights queries run as, set with `EXECUTE_AS_ROLE`. Empty for a service in a standard database. |
| `min_instances` | Minimum instance count. `1` when not set. |
| `max_instances` | Maximum instance count. Matches `MIN_INSTANCES` when not set. |
| `current_instances` | Current number of running instances. |

Expand

Show lessSee more

## Examples

Copy code

```
SHOW APPLICATION SERVICES IN SCHEMA my_db.my_schema;
```
