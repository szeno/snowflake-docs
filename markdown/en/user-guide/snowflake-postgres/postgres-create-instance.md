# Creating a Snowflake Postgres Instance

## Overview

You can create Snowflake Postgres instances by using either Snowsight or by executing
Snowflake SQL statements. You can configure the size of the instance, the storage size, and the
Postgres major version when creating an instance. You can also apply network policies to instances
at creation time.

## Privileges

To create Snowflake Postgres instances, you must use a role that has been granted
the CREATE POSTGRES INSTANCE privilege on the account. By default, this
privilege is granted to the ACCOUNTADMIN role.

To grant this privilege to other roles, a user with the ACCOUNTADMIN role
can run the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command:

Copy code

```
GRANT CREATE POSTGRES INSTANCE ON ACCOUNT TO your_role;
```

## Creating a Postgres instance

SnowsightSQL

You can create a Postgres instance by using the **Create** menu or by using the **Create** button in the **Postgres Instances** page.

**Using the main Create menu:**

1. At the top of the navigation menu, select [![Add a dashboard tile](/static/images/snowsight/snowsight-dashboards-add-tile-icon.png)](/static/images/snowsight/snowsight-dashboards-add-tile-icon.png) (**Create**).
2. Select **Postgres Instance**.
3. Configure your instance.
4. Select **Create**.

**Using the Create button on the Postgres instances page:**

1. In the navigation menu, select **Postgres**.
2. In the **Postgres Instances** page, select the **Create** button at the top right.
3. Choose your instance configuration.
4. Select **Create**.

![Create a Snowflake Postgres instance](/static/images/snowflake-postgres/new-snowflake-postgres-instance.png)

When you create an instance, the connection details are displayed, including the hostname and credentials needed to connect to
the instance. Save these credentials in a secure location; they will not be shown again. You can regenerate credentials later if
needed.

If you did not select a network policy, you will have the option to configure network settings from the instance details page.
See [Snowflake Postgres networking](/user-guide/snowflake-postgres/postgres-network) for more details.

![Snowflake Postgres connection reveal](/static/images/snowflake-postgres/snowflake-postgres-snowsight-connection.png)

> Use the [CREATE POSTGRES INSTANCE](/sql-reference/sql/create-postgres-instance) command to create a new Postgres instance. The syntax of this command is shown below:

Copy code

```
CREATE POSTGRES INSTANCE [ IF NOT EXISTS ] <name>
  COMPUTE_FAMILY = '<compute_family>'
  STORAGE_SIZE_GB = <storage_gb>
  AUTHENTICATION_AUTHORITY = { POSTGRES | POSTGRES_OR_SNOWFLAKE }
  [ POSTGRES_VERSION = { 16 | 17 | 18 } ]
  [ NETWORK_POLICY = '<network_policy>' ]
  [ HIGH_AVAILABILITY = { TRUE | FALSE } ]
  [ POSTGRES_SETTINGS = '<json_string>' ]
  [ COMMENT = '<string_literal>' ];
```

For the command parameters:

> `IF NOT EXISTS`
> :   Creates the instance only if an instance with the same name does not already exist. If an instance
>     with the same name already exists, the command does nothing and completes successfully. Useful for
>     idempotent scripts and automation.
>
> `COMPUTE_FAMILY = compute_family`
> :   Specifies the name of an instance size from the [Snowflake Postgres Instance Sizes](/user-guide/snowflake-postgres/postgres-instance-sizes) tables.
>
> `STORAGE_SIZE_GB = storage_gb`
> :   Specifies storage size in GB. Must be between 10 and 65,535.
>
> `AUTHENTICATION_AUTHORITY = { POSTGRES | POSTGRES_OR_SNOWFLAKE }`
> :   Specifies the authentication method for the instance. POSTGRES indicates that only Postgres user passwords can be used.
>     POSTGRES\_OR\_SNOWFLAKE also allows the use of short-lived access token passwords. See
>     [Snowflake Token Authentication for Snowflake Postgres](/user-guide/snowflake-postgres/postgres-token-auth) for more details.
>
> `POSTGRES_VERSION = { 16 | 17 | 18 }`
> :   Specifies the version of Postgres to use.
>
>     Default: The latest Postgres version.
>
> `NETWORK_POLICY = 'network_policy'`
> :   Specifies the [network policy](/user-guide/snowflake-postgres/postgres-network) to use for the instance. To specify this parameter, you must have been granted the USAGE privilege on the NETWORK\_POLICY object.
>
>     Default: No network policy is applied. A network policy will need to be configured before the instance can be reached. See [Snowflake Postgres networking](/user-guide/snowflake-postgres/postgres-network) for more information.
>
> `HIGH_AVAILABILITY = { TRUE | FALSE }`
> :   Specifies whether to enable high availability for the instance.
>
>     Default: `FALSE`
>
> `POSTGRES_SETTINGS = 'json_string'`
> :   Allows you to optionally set Postgres configuration parameters on your instance in JSON format. See [Snowflake Postgres Server Settings](/user-guide/snowflake-postgres/postgres-server-settings) for a list of available Postgres parameters.
>
>     Copy code
>
>     ```
>     '{"component:name" = "value", ...}'
>     ```
>
>     Default: No custom Postgres configuration parameters are set.
>
> `COMMENT = 'string_literal'`
> :   Specifies a comment for the Postgres instance.
>
>     Default: `NULL`

When you create the instance, one row with the following columns is returned:

- `status`
- `host`
- `access_roles`
- `default_database`

The `access_roles` column contains the user name and password for both the `snowflake_admin` and `application` roles. Save these details in a secure location because they cannot be retrieved later.

Creating a new instance takes some time to complete. The instance displays its current
state as it is building. See the list of [instance states](#instance-states) for
details about the states that you see while instances are being created.
