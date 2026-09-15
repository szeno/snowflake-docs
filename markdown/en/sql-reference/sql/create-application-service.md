# CREATE APPLICATION SERVICE

Creates a new Application Service that deploys a packaged application build from an
[artifact repository](/sql-reference/sql/create-artifact-repository).

An Application Service is a first-class Snowflake object. It manages its own
compute, lifecycle, and access control. Unlike a
[Snowpark Container Services service](/sql-reference/sql/create-service), an Application Service deploys from a
versioned package rather than from a user-supplied service specification.

See also:
:   [ALTER APPLICATION SERVICE](/sql-reference/sql/alter-application-service),
    [DESCRIBE APPLICATION SERVICE](/sql-reference/sql/desc-application-service),
    [DROP APPLICATION SERVICE](/sql-reference/sql/drop-application-service),
    [SHOW APPLICATION SERVICES](/sql-reference/sql/show-application-services)

## Syntax

Copy code

```
CREATE APPLICATION SERVICE [ IF NOT EXISTS ] <name>
  FROM ARTIFACT REPOSITORY <repository_name> PACKAGE <package_name>
  [ VERSION <version_alias> ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
  [ QUERY_WAREHOUSE = <warehouse_name> ]
  [ EXECUTE_AS_ROLE = <role_name> ]
  [ AUTO_RESUME = { TRUE | FALSE } ]
  [ AUTO_SUSPEND_SECS = <num> ]
  [ MIN_INSTANCES = <num> ]
  [ MAX_INSTANCES = <num> ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Specifies the identifier for the Application Service. The identifier must be
    unique for the schema where the service is created. For more details, see
    [Identifier requirements](/sql-reference/identifiers-syntax).

    The Application Service doesn’t share a namespace with SPCS `SERVICE`
    objects.

`FROM ARTIFACT REPOSITORY repository_name PACKAGE package_name`
:   Specifies the artifact repository and package to deploy. The repository must
    be of type `APPLICATION`.

    You must include `FROM ARTIFACT REPOSITORY`. Omitting the repository clause
    isn’t supported.

## Optional parameters

`VERSION version_alias`
:   Specifies the version of the package to deploy. You can pass a version name,
    such as `VERSION$3`, or a version alias, such as `LATEST` or
    `DEFAULT`. If you don’t specify a version, Snowflake uses the package’s
    default version; if the package has no default version, the command returns
    an error.

`EXTERNAL_ACCESS_INTEGRATIONS = ( integration_name [ , ... ] )`
:   Specifies the names of the
    [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access)
    that allow the application to access external network locations. The names
    in this list are case-sensitive.

`QUERY_WAREHOUSE = warehouse_name`
:   Specifies the warehouse used by the application when a container connects
    to Snowflake without explicitly specifying a warehouse.

`EXECUTE_AS_ROLE = role_name`
:   Specifies the role that Snowflake uses to run owner’s rights queries from the
    app and to derive caller’s rights grants. Only valid for an app created in a
    [personal database](/user-guide/personal-databases).

    Requirements:

    - The specified role must be granted to the owning user of the app.
    - If omitted, Snowflake sets `EXECUTE_AS_ROLE` to the creator’s session
      primary role.

    If the specified role is no longer granted to the owning user when the app starts,
    startup fails.

`AUTO_RESUME = { TRUE | FALSE }`
:   Specifies whether Snowflake automatically resumes the service when it
    receives an inbound request to one of its endpoints.

`AUTO_SUSPEND_SECS = num`
:   Specifies the number of seconds of inactivity after which Snowflake
    automatically suspends the Application Service. The minimum non-zero value
    is `300`. A value of `0` disables auto-suspend.

    **DEFAULT:** `0` (disabled)

`MIN_INSTANCES = num`
:   Specifies the minimum number of instances Snowflake keeps running.
    Snowflake never runs fewer than this, even if the app is idle.

    - Must be at least 1.
    - Can’t be greater than `MAX_INSTANCES`.

    **DEFAULT:** Not set. Defaults to `1` when `MAX_INSTANCES` is set. If both
    are unset, Snowflake runs one instance.

`MAX_INSTANCES = num`
:   Specifies the maximum number of instances Snowflake runs. Snowflake
    never runs more than this.

    - Must be at least 1 and no more than `10`.
    - Can’t be less than `MIN_INSTANCES`.

    **DEFAULT:** Not set. If unset, this matches `MIN_INSTANCES`.

`COMMENT = 'string_literal'`
:   Specifies a comment for the Application Service.

## Access control requirements

If your role does not own the objects in the following table, then your role
must have the listed
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) on those objects:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE APPLICATION SERVICE | Schema | Required to create a new Application Service in the schema. |
| READ | Artifact repository | Required on the artifact repository that contains the package. |
| USAGE | External access integration | Required for each integration listed in `EXTERNAL_ACCESS_INTEGRATIONS`. |
| USAGE | Warehouse | Required if `QUERY_WAREHOUSE` is specified. |
| USAGE | Role | Required on the role specified in `EXECUTE_AS_ROLE`. The role must be granted to the owning user of the app. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The Application Service starts automatically after creation. To check its
  status, use [SHOW APPLICATION SERVICES](/sql-reference/sql/show-application-services) or
  [DESCRIBE APPLICATION SERVICE](/sql-reference/sql/desc-application-service).
- To upgrade the service to a different package version, use
  [ALTER APPLICATION SERVICE](/sql-reference/sql/alter-application-service) with `UPGRADE`.
- Standalone SPCS SQL commands, such as `CREATE SERVICE` and `EXECUTE JOB SERVICE`, aren’t used to manage an Application Service. Use `APPLICATION SERVICE` commands instead.
- `CREATE OR REPLACE` isn’t supported for Application Services.
- You must specify `FROM ARTIFACT REPOSITORY` with the repository name. Commands
  that specify only `FROM PACKAGE` without a repository aren’t supported.
- Snowflake App Runtime isn’t available on
  [trial accounts](/user-guide/admin-trial-account).
- `EXECUTE_AS_ROLE` is set at creation time and can’t be changed with
  [ALTER APPLICATION SERVICE](/sql-reference/sql/alter-application-service).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Deploy the default version of a package from an artifact repository:

Copy code

```
CREATE APPLICATION SERVICE my_app
  FROM ARTIFACT REPOSITORY my_app_repo PACKAGE web_ui;
```

Deploy a specific version:

Copy code

```
CREATE APPLICATION SERVICE my_app
  FROM ARTIFACT REPOSITORY my_app_repo PACKAGE web_ui
  VERSION VERSION$3
  EXTERNAL_ACCESS_INTEGRATIONS = ( my_eai )
  QUERY_WAREHOUSE = my_warehouse
  AUTO_RESUME = TRUE
  AUTO_SUSPEND_SECS = 600
  COMMENT = 'Customer portal';
```

Deploy the `LATEST` alias:

Copy code

```
CREATE APPLICATION SERVICE my_app
  FROM ARTIFACT REPOSITORY my_app_repo PACKAGE web_ui
  VERSION LATEST;
```

Deploy in a personal database with a named execution role:

Copy code

```
CREATE APPLICATION SERVICE my_db.my_schema.my_app
  FROM ARTIFACT REPOSITORY my_app_repo PACKAGE web_ui
  EXECUTE_AS_ROLE = my_app_role;
```

Deploy with 2 to 5 instances:

Copy code

```
CREATE APPLICATION SERVICE my_app
  FROM ARTIFACT REPOSITORY my_app_repo PACKAGE web_ui
  VERSION LATEST
  MIN_INSTANCES = 2
  MAX_INSTANCES = 5;
```
