# SHOW IMAGE REPOSITORIES

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Lists the [image repositories](/developer-guide/snowpark-container-services/tutorials/tutorial-1) for which you
have access privileges.

You can use this command to list the repositories in the current database and schema for the session, a specified database or
schema, or your entire account.

See also:
:   [CREATE IMAGE REPOSITORY](/sql-reference/sql/create-image-repository) , [DROP IMAGE REPOSITORY](/sql-reference/sql/drop-image-repository)

## Syntax

Copy code

```
SHOW IMAGE REPOSITORIES [ LIKE '<pattern>' ]
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

## Access control requirements

Any of the following repository privileges grants the permission to see repositories in the SHOW IMAGE REPOSITORIES output. If you
don’t have any of these privileges, SHOW IMAGE REPOSITORIES will return an empty result.

| Privilege | Object | Notes |
| --- | --- | --- |
| READ | Image repository | To pull an image from a repository, the role requires this permission. |
| WRITE | Image repository | To push an image to a repository, the role requires this permission. |
| OWNERSHIP | Image repository | To create a repository, the role requires this permission. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

The command output provides repository properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the repository was created. |
| `database_name` | Database in which the repository was created. |
| `schema_name` | Schema in which the repository was created. |
| `repository_url` | URL of the image repository. You need this URL to push (for example, `docker push`) or pull (for example, `docker pull`) images from the repository. |
| `owner` | Role that owns the repository. |
| `owner_role_type` | The type of role that owns the object; either ROLE or DATABASE\_ROLE. |
| `comment` | Description for the repository. |
| `encryption` | Encryption type configured for the image repository. |
| `privatelink_repository_url` | URL of the image repository, accessible only via Private Connectivity. The column is returned only for [Business Critical](/user-guide/intro-editions) accounts. |

Expand

Show lessSee more

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

## Examples

The following two examples list repositories in the current database and current schema:

Copy code

```
SHOW IMAGE REPOSITORIES;
```

Copy code

```
SHOW IMAGE REPOSITORIES IN SCHEMA;
```

The following example lists repositories in the current database and the specified schema:

Copy code

```
SHOW IMAGE REPOSITORIES IN SCHEMA sc1;
```

The following example lists repositories in the current database and all schemas:

Copy code

```
SHOW IMAGE REPOSITORIES IN DATABASE;
```

The following example lists repositories in the specified database and all schemas:

Copy code

```
SHOW IMAGE REPOSITORIES IN DATABASE db1;
```

The following example lists repositories in the current account (all databases and all schemas):

Copy code

```
SHOW IMAGE REPOSITORIES IN ACCOUNT;
```

Sample output:

```
+-------------------------------+---------------------+---------------+-------------+-----------------------------------------------------------------------------------------------------------------------+-----------+-----------------+---------+---------------+--------------------------------------------------------------+
| created_on                    | name                | database_name | schema_name | repository_url                                                                                                        | owner     | owner_role_type | comment | encryption    | privatelink_repository_url                                   |
|-------------------------------+---------------------+---------------+-------------+-----------------------------------------------------------------------------------------------------------------------+-----------+-----------------+---------+---------------|--------------------------------------------------------------+
| 2024-04-18 13:41:53.481 -0700 | TUTORIAL_REPOSITORY | TUTORIAL_DB   | DATA_SCHEMA | orgname-acctname.registry-dev.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository                      | TEST_ROLE | ROLE            |         | SNOWFLAKE_SSE | orgname-acctname.registry.privatelink.snowflakecomputing.com |
+-------------------------------+---------------------+---------------+-------------+-----------------------------------------------------------------------------------------------------------------------+-----------+-----------------+---------+---------------+--------------------------------------------------------------+
```
