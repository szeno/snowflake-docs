# CREATE APPLICATION SERVICE

Creates a new Application Service that deploys a packaged application build from an
[artifact repository](/sql-reference/sql/create-artifact-repository).

An Application Service is a first-class Snowflake object. It manages its own
compute, lifecycle, and access control. Unlike a
[Snowpark Container Services service](/sql-reference/sql/create-service), an Application Service deploys from a
versioned package rather than from a user-supplied service specification.

This command supports the following variants:

- [CREATE OR ALTER APPLICATION SERVICE](#label-create-or-alter-application-service-syntax): Creates an Application Service
  if it doesn’t exist, or converges an existing one to the state described by a
  `SPECIFICATION`.

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
  [ SPECIFICATION = '<yaml>' ]
```

## Variant syntax

### CREATE OR ALTER APPLICATION SERVICE

Creates an Application Service if it doesn’t already exist, or converges an existing
Application Service to the state described in the statement. The `SPECIFICATION` is
the full intended state of the service: Snowflake computes the changes needed to reach
it, and resets any property the specification doesn’t set.

`CREATE OR ALTER APPLICATION SERVICE` requires a `SPECIFICATION`. It’s the only way to
update a specification, because
[ALTER APPLICATION SERVICE](/sql-reference/sql/alter-application-service) can’t set one.

For more information, see [CREATE OR ALTER APPLICATION SERVICE usage notes](#label-create-or-alter-application-service-usage-notes)
and [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE OR ALTER APPLICATION SERVICE <name>
  FROM ARTIFACT REPOSITORY <repository_name> PACKAGE <package_name>
  [ VERSION <version_alias> ]
  [ COMMENT = '<string_literal>' ]
  SPECIFICATION = '<yaml>'
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

`SPECIFICATION = 'yaml'`
:   Specifies an inline manifest that configures the service, as a single-quoted string
    or a dollar-quoted (`$$ ... $$`) block. When you supply a specification, Snowflake
    uses it as the source of truth for the properties it owns and doesn’t read the
    manifest packaged in the artifact repository.

    A specification is required with
    [CREATE OR ALTER APPLICATION SERVICE](#label-create-or-alter-application-service-syntax) and optional with
    `CREATE APPLICATION SERVICE`.

    The specification accepts the following keys. Unknown keys are an error, so a typo
    such as `min_instance` fails rather than being silently ignored.

    `version`
    :   The schema version of the specification. The only supported value is `2`.

        **DEFAULT:** `2`

    `label`, `description`, `icon`
    :   The display name, description, and icon for the app. `icon` is a path relative to the
        project root and can’t escape it with `../`. These values appear in the
        `additional_properties` column of
        [SHOW APPLICATION SERVICES](/sql-reference/sql/show-application-services) and
        [DESCRIBE APPLICATION SERVICE](/sql-reference/sql/desc-application-service).

    `query_warehouse`
    :   Equivalent to `QUERY_WAREHOUSE`.

    `min_instances`, `max_instances`
    :   Equivalent to `MIN_INSTANCES` and `MAX_INSTANCES`.

    `auto_resume`, `auto_suspend_secs`
    :   Equivalent to `AUTO_RESUME` and `AUTO_SUSPEND_SECS`.

    `execute_as_role`
    :   Equivalent to `EXECUTE_AS_ROLE`. Applied when the service is created. You can’t change
        it later, including with `CREATE OR ALTER`.

    `external_access_integrations`
    :   A list of external access integration names, equivalent to
        `EXTERNAL_ACCESS_INTEGRATIONS`.

    `secrets`
    :   A list of secrets to expose to the app. Each entry has a `name` (the name the app
        reads) and a `secret` (the identifier of the Snowflake secret object). Each secret
        must exist and be accessible to the owning role.

    `environment_variables`
    :   A list of environment variables to set in the app’s containers. Each entry has a
        `name` and a `value`.

    Properties that the specification owns can’t also appear as top-level clauses in the
    same statement. Specifying `QUERY_WAREHOUSE`, `EXTERNAL_ACCESS_INTEGRATIONS`,
    `MIN_INSTANCES`, `MAX_INSTANCES`, `AUTO_RESUME`, `AUTO_SUSPEND_SECS`, or
    `EXECUTE_AS_ROLE` alongside `SPECIFICATION` returns an error that tells you to set the
    property inside the specification instead. `COMMENT` isn’t owned by the specification,
    so you set it as a top-level clause.

## Access control requirements

If your role does not own the objects in the following table, then your role
must have the listed
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) on those objects:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE APPLICATION SERVICE | Schema | Required to create a new Application Service in the schema. |
| READ | Artifact repository | Required on the artifact repository that contains the package. |
| USAGE | External access integration | Required for each integration listed in `EXTERNAL_ACCESS_INTEGRATIONS` or in the `external_access_integrations` key of a `SPECIFICATION`. |
| USAGE | Warehouse | Required if `QUERY_WAREHOUSE` is specified, including as `query_warehouse` in a `SPECIFICATION`. |
| USAGE | Role | Required on the role specified in `EXECUTE_AS_ROLE`, including as `execute_as_role` in a `SPECIFICATION`. The role must be granted to the owning user of the app. |
| OWNERSHIP | Application Service | Required when `CREATE OR ALTER APPLICATION SERVICE` alters an existing Application Service. |
| READ | Secret | Required on each secret listed in the `secrets` key of a `SPECIFICATION`. |

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
- `CREATE OR REPLACE` isn’t supported for Application Services. To create a service if
  it doesn’t exist or update it if it does, use
  [CREATE OR ALTER APPLICATION SERVICE](#label-create-or-alter-application-service-syntax).
- You must specify `FROM ARTIFACT REPOSITORY` with the repository name. Commands
  that specify only `FROM PACKAGE` without a repository aren’t supported.
- Snowflake App Runtime isn’t available on
  [trial accounts](/user-guide/admin-trial-account).
- `EXECUTE_AS_ROLE` is set at creation time and can’t be changed with
  [ALTER APPLICATION SERVICE](/sql-reference/sql/alter-application-service).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## CREATE OR ALTER APPLICATION SERVICE usage notes

- A `SPECIFICATION` is required. `CREATE OR ALTER APPLICATION SERVICE` without one
  returns an error.
- `CREATE OR ALTER` can’t be combined with `IF NOT EXISTS`.
- The specification is the full intended state of the service. Snowflake resets every
  property the specification owns but doesn’t set:

  - Omitting `label`, `description`, or `icon` clears it.
  - Omitting `external_access_integrations`, `secrets`, or `environment_variables`
    removes all of them.
  - Omitting `auto_suspend_secs`, `min_instances`, or `max_instances` returns it to its
    default.
  - Omitting `query_warehouse` unsets it.
  - Omitting `auto_resume` returns it to its default.

  To keep a value, restate it in every `CREATE OR ALTER` statement.
- `execute_as_role` is applied when the service is created and can’t be changed
  afterward. Sending a different value for an existing service returns an error;
  omitting it leaves the current role in place.
- The package and the artifact repository are fixed when the service is created. Naming
  a different package or repository for an existing service returns an error.
  Re-sending the current value is a no-op.
- When you include a `VERSION` clause, Snowflake converges the service to that version
  after applying the specification. Because a version alias is resolved at statement
  time, `VERSION LATEST` picks up a newer version if one has been published since the
  last deployment.
- A specification can’t be read back. It isn’t shown by
  [DESCRIBE APPLICATION SERVICE](/sql-reference/sql/desc-application-service) or
  [SHOW APPLICATION SERVICES](/sql-reference/sql/show-application-services), and
  [GET\_DDL](/sql-reference/functions/get_ddl) doesn’t support Application Services. Keep the
  specification in source control. For CLI deploys that’s the service-level keys in
  `app.yml`; if you write the SQL yourself, send only the keys listed under
  `SPECIFICATION`. You can’t pass a whole `app.yml` as a specification. For more
  information, see
  [Validation](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-validation).
- `CREATE OR ALTER APPLICATION SERVICE` requires the `FROM ARTIFACT REPOSITORY` clause.

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

Create the service if it doesn’t exist, or converge it to this state if it does:

Copy code

```
CREATE OR ALTER APPLICATION SERVICE my_db.my_schema.my_app
  FROM ARTIFACT REPOSITORY my_app_repo PACKAGE web_ui
  VERSION LATEST
  SPECIFICATION = $$
label: "My App"
description: "Production instance of My App."
icon: public/icon.svg
query_warehouse: my_warehouse
min_instances: 1
max_instances: 3
auto_resume: true
auto_suspend_secs: 600
external_access_integrations:
  - stripe_eai
  - logging_eai
secrets:
  - name: STRIPE_API_KEY
    secret: my_db.my_schema.stripe_secret
environment_variables:
  - name: LOG_LEVEL
    value: "INFO"
$$;
```

Because the specification is the full intended state, this next statement changes the
warehouse and drops everything else the previous statement set. The integrations and
the secret are removed, the label and description are cleared, and `max_instances` and
`auto_suspend_secs` return to their defaults:

Copy code

```
CREATE OR ALTER APPLICATION SERVICE my_db.my_schema.my_app
  FROM ARTIFACT REPOSITORY my_app_repo PACKAGE web_ui
  VERSION LATEST
  SPECIFICATION = $$
query_warehouse: my_other_warehouse
$$;
```

Redeploy after publishing a new build. Resolving `LATEST` again moves the service to
the new version, and restating the specification in full leaves everything else
unchanged:

Copy code

```
CREATE OR ALTER APPLICATION SERVICE my_db.my_schema.my_app
  FROM ARTIFACT REPOSITORY my_app_repo PACKAGE web_ui
  VERSION LATEST
  COMMENT = 'Redeployed after the nightly build'
  SPECIFICATION = $$
label: "My App"
description: "Production instance of My App."
icon: public/icon.svg
query_warehouse: my_warehouse
min_instances: 1
max_instances: 3
auto_resume: true
auto_suspend_secs: 600
external_access_integrations:
  - stripe_eai
  - logging_eai
secrets:
  - name: STRIPE_API_KEY
    secret: my_db.my_schema.stripe_secret
environment_variables:
  - name: LOG_LEVEL
    value: "INFO"
$$;
```
