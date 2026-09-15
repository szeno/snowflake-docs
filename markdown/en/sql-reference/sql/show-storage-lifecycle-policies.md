# SHOW STORAGE LIFECYCLE POLICIES

Lists the [storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies) for which you have access privileges.

You can use this command to list objects in the current database and schema for the session, a specified database or schema, or
your entire account.

The output includes the metadata and properties for each object. The objects are sorted lexicographically by database, schema,
and object name (see Output in this topic for descriptions of the output columns). The order of rows in the results is important
to note if you want to filter the results.

See also:
:   [CREATE STORAGE LIFECYCLE POLICY](/sql-reference/sql/create-storage-lifecycle-policy) , [ALTER STORAGE LIFECYCLE POLICY](/sql-reference/sql/alter-storage-lifecycle-policy) , [DESCRIBE STORAGE LIFECYCLE POLICY](/sql-reference/sql/desc-storage-lifecycle-policy) , [DROP STORAGE LIFECYCLE POLICY](/sql-reference/sql/drop-storage-lifecycle-policy)

## Syntax

Copy code

```
SHOW STORAGE LIFECYCLE POLICIES
  [ LIKE '<pattern>' ]
  [ IN
        {
          ACCOUNT                  |

          DATABASE                 |
          DATABASE <database_name> |

          SCHEMA                   |
          SCHEMA <schema_name>     |
          <schema_name>
        }
  ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns records for the entire account.

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or for a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

        Note

        Using SHOW commands without an `IN` clause in a database context can result in fewer than expected results.

        Objects with the same name are only displayed once if no `IN` clause is used. For example, if you have table `t1` in
        `schema1` and table `t1` in `schema2`, and they are both in scope of the database context you’ve specified (that is, the database
        you’ve selected is the parent of `schema1` and `schema2`), then SHOW TABLES only displays one of the `t1` tables.

    `SCHEMA`, `SCHEMA schema_name`
    :   Returns records for the current schema in use or a specified schema (`schema_name`).

        `SCHEMA` is optional if a database is in use or if you specify the fully qualified `schema_name` (for example, `db.schema`).

        If no database is in use, specifying `SCHEMA` has no effect on the output.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `created_on` | Date and time the policy was created. |
| `name` | The name of the policy. |
| `database_name` | The name of the database the policy is associated with. |
| `schema_name` | The name of the schema the policy uses. |
| `kind` | The type of storage lifecycle policy. |
| `owner` | The name of the role that created the policy. |
| `comment` | An optional comment that describes the policy. |
| `owner_role_type` | The type of role that the owner of the policy used to create the policy. |
| `options` | Optional parameters added to the policy to change how the policy behaves:   - `archive_for_days`: Number of days to archive rows before expiration. If this property isn’t set for the policy, the value is NULL. - `archive_tier`: The storage tier for the policy; COOL or COLD. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY STORAGE LIFECYCLE POLICY | Account | Allows SHOW on all storage lifecycle policies in the account. |
| APPLY | Storage lifecycle policy | Allows SHOW on the policy. |
| OWNERSHIP | Storage lifecycle policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

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

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

- Executing the command for schema-level objects only returns an object if the current role also has at least one privilege on the
  parent database and schema.

## Examples

The following example lists the storage lifecycle policies that you have the privileges to view in the PUBLIC schema of the `mydb`
database:

Copy code

```
USE DATABASE mydb;

SHOW STORAGE LIFECYCLE POLICIES;
```

Output:

```
+----------------------------------------+------------------+---------------------------+-------------------------------+--------------------------+--------------+-------------------+-----------------+---------------------------+
|               created_on               |       name       |       database_name       |          schema_name          |           kind           |    owner     |      comment      | owner_role_type |          options          |
+----------------------------------------+------------------+---------------------------+-------------------------------+--------------------------+--------------+-------------------+-----------------+---------------------------+
| Fri, 23 Jun 1967 07:00:00.123000 +0000 | MY_POLICY        | MYDB                      | PUBLIC                        | STORAGE_LIFECYCLE_POLICY | TESTACCOUNT  | identity          | ROLE            | {"ARCHIVE_FOR_DAYS":null} |
| Fri, 23 Jun 1967 07:00:00.123000 +0000 | MY_SECOND_POLICY | MYDB                      | PUBLIC                        | STORAGE_LIFECYCLE_POLICY | TESTACCOUNT  | identity with UDF | ROLE            | {"ARCHIVE_FOR_DAYS":365}  |
| Fri, 23 Jun 1967 07:00:00.123000 +0000 | MY_THIRD_POLICY  | MYDB                      | PUBLIC                        | STORAGE_LIFECYCLE_POLICY | TESTACCOUNT  | always true       | ROLE            | {"ARCHIVE_FOR_DAYS":180}  |
+----------------------------------------+------------------+---------------------------+-------------------------------+--------------------------+--------------+-------------------+-----------------+---------------------------+
```
