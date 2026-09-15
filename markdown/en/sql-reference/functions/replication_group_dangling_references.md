Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# REPLICATION\_GROUP\_DANGLING\_REFERENCES

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Detects cases where an object that’s referenced in a replication group or failover group isn’t actually replicated to the secondary
account. Snowflake refers to these types of references as *dangling references*.

After you use this function to detect dangling references in your replication configuration, you can
rearrange your replication groups or failover groups so that all of the referenced objects are included.
Or, you can modify your SQL object hierarchy so that the referenced objects are part of a container
such as a database or schema that’s included in the replication groups or failover groups.

If you use multiple replication groups or failover groups, you might also specify the order of
refresh operations to make sure that any objects that are required to resolve dangling references
are replicated to the secondary account before the objects that refer to them.

Important

Pay special attention to any TRUE values in the IS\_BLOCKING\_REFRESH column.
Both refresh and failover operations can’t proceed until you resolve those
references.

See also:
:   [Replication and references across replication groups](/user-guide/account-replication-considerations#label-references-across-replication-groups)

## Syntax

Copy code

```
REPLICATION_GROUP_DANGLING_REFERENCES( '<replication_or_failover_group_name>' )
```

## Arguments

`'replication_or_failover_group_name'`
:   Name of the replication group or failover group to check for dangling references.
    The entire name must be enclosed in single quotes.

## Output

The function returns the following columns.

| Column Name | Data Type | Description |
| --- | --- | --- |
| REFERENCED\_ENTITY\_DOMAIN | VARCHAR | The domain of the entity referred to by the dangling reference. |
| REFERENCED\_ENTITY\_NAME | VARCHAR | The fully qualified name of the entity referred to by the dangling reference. |
| REFERENCING\_ENTITY\_DOMAIN | VARCHAR | The domain of the entity in the replication group with a dangling reference, for example, `Table`. |
| REFERENCING\_ENTITY\_NAME | VARCHAR | The fully qualified name of the entity in the replication group with a dangling reference. |
| REFERENCING\_ENTITY\_GROUPS | VARCHAR | A comma-separated list of all replication groups that contain the referencing entity, or NULL if no group contains that entity. |
| IS\_BLOCKING\_REFRESH | BOOLEAN | If TRUE, replication refreshes and failovers will fail until this reference is resolved. If FALSE, Snowflake can perform those operations despite the dangling reference. |

Expand

Show lessSee more

## Usage notes

- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema
  in use or the function name must be fully-qualified.
  For more information, see [Snowflake Information Schema](/sql-reference/info-schema).
- You can run this function from any account in your organization.
  The replication group or failover group that you specify must exist in the account that calls the function.
  That is, you specify the group name that’s used in the cloud service provider region where you call the function.

  - If the function is called using a replication group or failover group on the primary account,
    it reports dangling references if their corresponding referred objects aren’t replicated to
    *all* the secondary accounts.
  - If the function is called using a replication group or failover group on the secondary account,
    it reports dangling references if their corresponding referred objects aren’t replicated to
    the specific secondary where the function was called.
- For information about how to deal with dangling references in replication groups and failover groups,
  see [Replication and references across replication groups](/user-guide/account-replication-considerations#label-references-across-replication-groups).

## Examples

To check for dangling references in the failover group `myfg`,
run the following statement from your primary or secondary account.

Copy code

```
SELECT *
  FROM TABLE(
      INFORMATION_SCHEMA.REPLICATION_GROUP_DANGLING_REFERENCES('myfg')
  );
```
