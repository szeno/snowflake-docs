# ALTER POSTGRES INSTANCE

Modifies the properties of an existing [Snowflake Postgres instance](/user-guide/snowflake-postgres/about).

See also:
:   [CREATE POSTGRES INSTANCE](/sql-reference/sql/create-postgres-instance), [DESCRIBE POSTGRES INSTANCE](/sql-reference/sql/desc-postgres-instance), [DROP POSTGRES INSTANCE](/sql-reference/sql/drop-postgres-instance), [SHOW POSTGRES INSTANCES](/sql-reference/sql/show-postgres-instances)

## Syntax

Copy code

```
ALTER POSTGRES INSTANCE [ IF EXISTS ] <name>
  RENAME TO <new_name>

ALTER POSTGRES INSTANCE [ IF EXISTS ] <name> SET
  [ NETWORK_POLICY = '<network_policy>' ]
  [ AUTHENTICATION_AUTHORITY = { POSTGRES | POSTGRES_OR_SNOWFLAKE } ]
  [ COMMENT = '<string_literal>' ]
  [ HIGH_AVAILABILITY = { TRUE | FALSE } ]
  [ COMPUTE_FAMILY = '<compute_family>' ]
  [ STORAGE_SIZE_GB = <storage_gb> ]
  [ STORAGE_INTEGRATION = '<storage_integration_name>' ]
  [ POSTGRES_VERSION = { 16 | 17 | 18 } ]
  [ MAINTENANCE_WINDOW_START = <hour_of_day> ]
  [ POSTGRES_SETTINGS = '<json_string>' ]
  [ APPLY { IMMEDIATELY | ON '<timestamp>' } ]

ALTER POSTGRES INSTANCE [ IF EXISTS ] <name>
  UNSET { COMMENT | POSTGRES_SETTINGS | NETWORK_POLICY
    | MAINTENANCE_WINDOW_START | STORAGE_INTEGRATION } [ , ... ]

ALTER POSTGRES INSTANCE [ IF EXISTS ] <name> SUSPEND

ALTER POSTGRES INSTANCE [ IF EXISTS ] <name> RESUME

ALTER POSTGRES INSTANCE [ IF EXISTS ] <name> RESET ACCESS
  FOR { 'snowflake_admin' | 'application' }

ALTER POSTGRES INSTANCE [ IF EXISTS ] <name> SET TAG <tag_name> =
  '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER POSTGRES INSTANCE [ IF EXISTS ] <name> UNSET TAG <tag_name>
  [ , <tag_name> ... ]
```

## Parameters

`name`
:   Specifies the identifier for the Postgres instance to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Changes the name of the Postgres instance to the specified new name. The new identifier must be unique for the account.

    For more details about identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RESET ACCESS FOR { 'snowflake_admin' | 'application' }`
:   Regenerates credentials for the `snowflake_admin` or `application` role. Returns one row with the following column:

    - `password`

    For more information, see [Snowflake Postgres Roles](/user-guide/snowflake-postgres/postgres-roles).

`SET ...`
:   Sets one or more specified properties for the Postgres instance:

    `NETWORK_POLICY = 'network_policy'`
    :   Specifies the [network policy](/user-guide/snowflake-postgres/postgres-network) to use for the instance.
        Changes to the policy may take up to 2 minutes to take effect.

        To specify this parameter, you must have been granted the USAGE privilege on the network policy object.

    `AUTHENTICATION_AUTHORITY = { POSTGRES | POSTGRES_OR_SNOWFLAKE }`
    :   Change the authentication method for the instance. POSTGRES indicates that only Postgres user passwords can be used.
        POSTGRES\_OR\_SNOWFLAKE also allows the use of short-lived access token passwords. See
        [Snowflake Token Authentication for Snowflake Postgres](/user-guide/snowflake-postgres/postgres-token-auth) for more details.

    `COMMENT = 'string_literal'`
    :   Adds or overwrites an existing comment for the Postgres instance.

    `HIGH_AVAILABILITY = { TRUE | FALSE }`
    :   Enables or disables [high availability](/user-guide/snowflake-postgres/high-availability) for the instance.
        Executes as an asynchronous operation. Run the DESCRIBE POSTGRES INSTANCE command and monitor the
        `operations` field to track progress.

        A high availability change can only be initiated if the instance is in the READY state and no other operation is running.

        Note

        Burstable instance sizes (BURST\_S, BURST\_M) do not support high availability. To enable HA, you must
        first change to a STANDARD or HIGHMEM compute family.

    `COMPUTE_FAMILY = 'compute_family'`
    :   Specifies the new [instance size](/user-guide/snowflake-postgres/postgres-instance-sizes) for the Postgres instance.

    `STORAGE_SIZE_GB = storage_gb`
    :   Specifies the new storage size in GB. Both increases and decreases are supported.

        Note

        When you decrease the storage size, you can’t set it too close to current disk usage. The new size must be
        at least 1.4x the disk space currently in use. That way, there’s still room to add more data without
        triggering an automatic storage increase.

    `STORAGE_INTEGRATION = 'storage_integration_name'`
    :   Attaches a storage integration of type `POSTGRES_EXTERNAL_STORAGE` to the Postgres instance,
        enabling the pg\_lake extension to access data in external object storage. For the complete setup
        procedure, see [pg\_lake](/user-guide/snowflake-postgres/postgres-pg_lake).

        [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

        Available to all accounts.

    `POSTGRES_VERSION = { 16 | 17 | 18 }`
    :   Specifies the Postgres major version to upgrade to. You can only upgrade to a newer version; downgrading isn’t supported.

    `MAINTENANCE_WINDOW_START = hour_of_day`
    :   Specifies the hour of day (0-23, UTC) when a maintenance window can start. Maintenance windows are three hours long,
        starting from the specified hour.

    `POSTGRES_SETTINGS = 'json_string'`
    :   Specifies changes to the [Postgres server settings](/user-guide/snowflake-postgres/postgres-server-settings)
        for the instance in JSON format:

        Copy code

        ```
        '{"component:name" = "value", ...}'
        ```

        Some settings require an instance restart to take effect. These changes won’t be applied unless you specify
        `APPLY IMMEDIATELY`.

    `APPLY IMMEDIATELY`
    :   Overrides any defined maintenance window and applies the specified operations as soon as they’re ready.
        Applies to `COMPUTE_FAMILY`, `STORAGE_SIZE_GB`, `POSTGRES_VERSION`, and `POSTGRES_SETTINGS`.

    `APPLY ON 'timestamp'`
    :   Overrides any defined maintenance window and applies the specified operations at the given timestamp.
        The timestamp can’t be more than 72 hours in the future.

        Supported timestamp formats:

        - `yyyy-MM-dd`
        - `yyyy-MM-dd HH:mm`
        - `yyyy-MM-dd HH:mm:ss`
        - `yyyy-MM-dd HH:mm zzz`

`UNSET ...`
:   Unsets one or more specified properties for the Postgres instance, resetting them to their defaults:

    - `COMMENT`
    - `POSTGRES_SETTINGS`
    - `NETWORK_POLICY`
    - `MAINTENANCE_WINDOW_START` - Unsetting causes all ongoing operations to be applied as soon as they’re completed.
    - `STORAGE_INTEGRATION` - Removes the storage integration from the instance, disabling pg\_lake access to external storage.

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

`SUSPEND`
:   Suspends the Postgres instance. The virtual machine is deactivated while the disk image is kept in storage.
    Normal billing is suspended, but storage costs continue to accrue. Existing backups are retained.

`RESUME`
:   Resumes a suspended Postgres instance. If there were operations pending restart, they’re applied when the instance resumes.

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or MODIFY | Postgres instance | Required for modifying instance properties. |
| OWNERSHIP or OPERATE | Postgres instance | Required for SUSPEND and RESUME acctions. |
| USAGE | Network policy | Required only if specifying a NETWORK\_POLICY. |
| USAGE | Storage integration | Required only if specifying a STORAGE\_INTEGRATION. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Changes to `COMPUTE_FAMILY`, `STORAGE_SIZE_GB`, and `POSTGRES_VERSION` are collectively referred to as
  “upgrade” operations and can be performed together. Run the DESCRIBE POSTGRES INSTANCE command and monitor the
  `operations` field to track progress.
- An upgrade operation can only be initiated if the instance is in the READY state and no other operation is running.
- If an instance has a defined maintenance window, changes won’t take effect until the maintenance window period starts,
  unless `APPLY IMMEDIATELY` is specified. Maintenance windows control *when* changes are applied, not whether
  the instance is running. For more details about maintenance operations, see
  [Snowflake Postgres instance management](/user-guide/snowflake-postgres/managing-instances).
- **A brief service interruption is required to perform instance management operations.** Ensure that your applications
  can automatically reconnect to the database.
- SUSPEND and RESUME are immediate operations for stopping and starting instance billing. They are distinct from
  maintenance windows, which schedule when configuration changes (like upgrades or HA enablement) take effect.
- The connection string for an instance remains the same across instance management operations, unless you explicitly
  regenerate credentials.
- An instance’s current network policy is considered an instance property, so changing it requires both OWNERSHIP or MODIFY
  on the instance and USAGE on the new network policy.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Change the compute family and storage size for a Postgres instance:

Copy code

```
ALTER POSTGRES INSTANCE my_postgres
  SET COMPUTE_FAMILY = 'STANDARD_M'
      STORAGE_SIZE_GB = 100;
```

Monitor the progress of the operation using DESCRIBE:

Copy code

```
DESCRIBE POSTGRES INSTANCE my_postgres
  ->> SELECT "property", "value"
      FROM $1
      WHERE "property" IN
        ('name', 'state', 'operations', 'compute_family',
          'storage_size_gb');

-- Repeat until state shows 'READY'
```

Enable high availability for an instance:

Copy code

```
-- Check current HA status
DESCRIBE POSTGRES INSTANCE my_postgres
  ->> SELECT "property", "value"
      FROM $1
      WHERE "property" IN ('name', 'high_availability',
        'state');

-- Enable HA (asynchronous operation)
ALTER POSTGRES INSTANCE my_postgres
  SET HIGH_AVAILABILITY = TRUE;

-- Monitor until operation completes
DESCRIBE POSTGRES INSTANCE my_postgres
  ->> SELECT "property", "value"
      FROM $1
      WHERE "property" IN ('name', 'high_availability',
        'state');
```

Upgrade to Postgres 18:

Copy code

```
-- Check current Postgres version using flow operator
SHOW POSTGRES INSTANCES
  ->> SELECT "name", "postgres_version", "state"
      FROM $1
      WHERE "name" = 'my_postgres';

-- Upgrade to version 18
ALTER POSTGRES INSTANCE my_postgres
  SET POSTGRES_VERSION = 18;
```

Apply changes immediately, overriding the maintenance window:

Copy code

```
ALTER POSTGRES INSTANCE my_postgres
  SET COMPUTE_FAMILY = 'STANDARD_L'
  APPLY IMMEDIATELY;
```

Suspend a Postgres instance:

Copy code

```
-- Check state before suspending
DESCRIBE POSTGRES INSTANCE my_postgres
  ->> SELECT "property", "value"
      FROM $1
      WHERE "property" IN ('name', 'state');

-- Suspend the instance
ALTER POSTGRES INSTANCE my_postgres SUSPEND;

-- Verify suspended state
DESCRIBE POSTGRES INSTANCE my_postgres
  ->> SELECT "property", "value"
      FROM $1
      WHERE "property" IN ('name', 'state');
```

Resume a suspended instance:

Copy code

```
ALTER POSTGRES INSTANCE my_postgres RESUME;
```

Rename a Postgres instance:

Copy code

```
ALTER POSTGRES INSTANCE my_postgres
  RENAME TO prod_postgres;
```

Note

Renaming an instance changes its identifier in Snowflake but does *not* change the connection hostname. The
hostname remains the same, so existing connections and applications continue to work without modification.
