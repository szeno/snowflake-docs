# CREATE SNAPSHOT

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Note

This operation is not currently covered by the Service Level set forth in
[Snowflake’s Support Policy and Service Level Agreement](https://www.snowflake.com/legal/support-policy-and-service-level-agreement/).

Creates or replaces a [snapshot of a block storage volume](/developer-guide/snowpark-container-services/block-storage-volume#label-snowpark-containers-block-storage-manage-snapshots) for a specified volume and service instance. The snapshot is created in the current schema.

See also:
:   [ALTER SNAPSHOT](/sql-reference/sql/alter-snapshot), [DESCRIBE SNAPSHOT](/sql-reference/sql/desc-snapshot), [DROP SNAPSHOT](/sql-reference/sql/drop-snapshot) , [SHOW SNAPSHOTS](/sql-reference/sql/show-snapshots)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] SNAPSHOT [ IF NOT EXISTS ] <name>
  FROM SERVICE <service_name>
  VOLUME "<volume_name>"
  INSTANCE <instance_id>
  [ COMMENT = '<string_literal>']
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
```

## Required parameters

`name`
:   String that specifies the identifier (that is, name) for the snapshot; must be unique for the schema in which the snapshot is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`FROM SERVICE service_name`
:   Specifies the name of the service.

`VOLUME "volume_name"`
:   Specifies the name of the volume associated with the service. Snapshots can only be taken for block storage volumes (and not for local, memory, or stage volumes).

    Volume names are case-sensitive. Therefore, double quotes should always be used to match the corresponding name in the service specification.

`INSTANCE instance_id`
:   Index of the service instance. The service instance index starts at 0 and the range is `[0, ..., MAX_INSTANCES - 1]`. You can call the [SYSTEM$GET\_SERVICE\_STATUS — Deprecated](/sql-reference/functions/system_get_service_status) function to get the relevant information.

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the service.

    Default: No value

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SNAPSHOT | Schema |  |
| OPERATE | Service |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Snowflake deletes job services approximately 10 minutes after its execution completes. To preserve the content of a block storage volume used by the job service, you must create a snapshot before Snowflake deletes the job. For example, you might use a stored procedure to first execute a job service and create a snapshot immediately following it.
- A schema cannot contain snapshots with the same name. When creating a snapshot, if a snapshot with the same name already exists in the schema, an error is returned and the snapshot is not created, unless the optional `OR REPLACE` keyword is included in the command, in which case Snowflake deletes the existing snapshot and creates a new snapshot.

  Important

  A snapshot deleted using the DROP SNAPSHOT or the CREATE OR REPLACE SNAPSHOT command cannot be restored. For volumes containing critical data, create new snapshots with unique names, such as using timestamps in the snapshot name.

## Examples

If you create a service with two instances (the number of containers isn’t relevant) with a volume named “data”, you would create a snapshot of the volume associated with the first instance using the following SQL:

Copy code

```
CREATE SNAPSHOT snapshot_0
  FROM SERVICE example_service
  VOLUME "data"
  INSTANCE 0
  COMMENT='new snapshot';
```

To create a snapshot of the volume associated with the second service instance, you specify `INSTANCE 1` in the preceding SQL.
