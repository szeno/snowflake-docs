# DESCRIBE STORAGE LIFECYCLE POLICY

Describes the properties of a [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE STORAGE LIFECYCLE POLICY](/sql-reference/sql/create-storage-lifecycle-policy) , [ALTER STORAGE LIFECYCLE POLICY](/sql-reference/sql/alter-storage-lifecycle-policy) , [DROP STORAGE LIFECYCLE POLICY](/sql-reference/sql/drop-storage-lifecycle-policy) , [SHOW STORAGE LIFECYCLE POLICIES](/sql-reference/sql/show-storage-lifecycle-policies)

## Syntax

Copy code

```
{ DESC | DESCRIBE } STORAGE LIFECYCLE POLICY <policy_name>
```

## Parameters

`policy_name`
:   Specifies the identifier for the policy to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `name` | The name of the policy. |
| `signature` | The columns the policy uses to evaluate rows for expiration. |
| `return_type` | A VARCHAR value that contains the data type of the return value. For example BOOLEAN, NUMBER, ARRAY, and OBJECT. |
| `body` | The function body that evaluates whether a row should be expired. |
| `archive_tier` | The archive storage tier; COOL or COLD. |
| `archive_for_days` | The (optional) number of days to archive table rows before expiration. If this property isn’t set, the value is NULL. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY STORAGE LIFECYCLE POLICY | Account | Allows DESC on all storage lifecycle policies in the account. |
| APPLY | Storage lifecycle policy | Allows DESC on the storage lifecycle policy. |
| OWNERSHIP | Storage lifecycle policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

- If you’ve ever enabled archive storage for a policy, the `archive_tier` property in the command output
  shows the archive tier (COOL or COLD) that was set. This is true even
  if you transition the archival policy into an expiration policy by using ALTER STORAGE LIFECYCLE POLICY to unset the ARCHIVE\_FOR\_DAYS parameter.
  You can’t change the archive tier after setting it.

## Examples

The following example describes the storage lifecycle policy named `my_storage_lifecycle_policy`:

Copy code

```
DESCRIBE STORAGE LIFECYCLE POLICY example_slp;
```

Output:

```
+-----------------------------+----------------+-------------+------+------------------+
| name                        | signature      | return_type | body | archive_for_days |
|-----------------------------+----------------+-------------+------+------------------|
| MY_STORAGE_LIFECYCLE_POLICY | (ARG1 BOOLEAN) | BOOLEAN     | arg1 |              365 |
+-----------------------------+----------------+-------------+------+------------------+
```
