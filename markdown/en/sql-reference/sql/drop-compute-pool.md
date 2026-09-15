# DROP COMPUTE POOL

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Removes the specified [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool) from the
account.

See also:
:   [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) , [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool), [DESCRIBE COMPUTE POOL](/sql-reference/sql/desc-compute-pool) , [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools)

## Syntax

Copy code

```
DROP COMPUTE POOL [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the compute pool to be dropped.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Compute pool |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When dropping a compute pool, Snowflake automatically aborts any running jobs. However, Snowflake does not drop running services.
  If services are running this command will fail. You need to explicitly drop all running services before dropping a compute pool.
  You can run [ALTER COMPUTE POOL … STOP ALL](/sql-reference/sql/alter-compute-pool), which drops both services and jobs. You can also use
  the [DROP SERVICE](/sql-reference/sql/drop-service) command to drop individual services.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

The following example drops the compute pool named `tutorial_compute_pool`:

Copy code

```
DROP COMPUTE POOL tutorial_compute_pool;
```

```
+---------------------------------------------+
| status                                      |
|---------------------------------------------|
| TUTORIAL_COMPUTE_POOL successfully dropped. |
+---------------------------------------------+
```
