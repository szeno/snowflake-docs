# SHOW CALLER GRANTS

Lists the [caller grants](/developer-guide/restricted-callers-rights#label-restricted-callers-rights-about-grants) being used to implement restricted caller’s rights.

## Syntax

Copy code

```
SHOW CALLER GRANTS
{
{ ON <object_type> <object_name> | ON ACCOUNT }
| TO { ROLE | DATABASE ROLE }  <owner_name>
}
```

## Parameters

`ON object_type object_name` or `ON ACCOUNT`
:   Specifies whether to list the caller grants on a specific object or list all caller grants involving the account.

    Use the singular form of `object_type`, for example, `TABLE` or `WAREHOUSE`.

`TO ROLE <owner_name>` or `TO DATABASE ROLE <owner_name>`
:   Specifies an executable owner, which lists all caller grants that have been granted to that owner.

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the caller grant was granted. |
| `privilege` | Privilege that executables owned by `grantee_name` can run with. |
| `granted_on` | Type of object that is subject to the caller grant, regardless of whether it was granted directly on an object or on all objects of that type. |
| `name` | If the caller grant was granted directly on a specific object, specifies the name of the object. |
| `is_inherited` | If `TRUE`, the caller grant was granted to all objects of a certain type using a GRANT INHERITED CALLER or GRANT ALL INHERITED CALLER PRIVILEGES statement.  If `FALSE`, the caller grant was granted directly on the `name` object. |
| `inherited_from` | If the caller grant was granted to all objects of a certain type using a GRANT INHERITED CALLER or GRANT ALL INHERITED CALLER PRIVILEGES statement, indicates the level at which it was granted. One of `ACCOUNT`, `DATABASE`, or `SCHEMA`. |
| `inherited_from_database` | If `inherited_from` is a database (including an application or application package), specifies the name of the database. If `inherited_from` is a schema, specifies the name of the database that contains the schema. |
| `inherited_from_schema` | If `inherited_from` is a schema, specifies the name of the schema. |
| `granted_to` | Type of executable owner to which the caller grant was granted. One of `ROLE` or `DATABASE ROLE`. |
| `grantee_name` | Name of the executable owner to which the caller grant was granted. |

Expand

Show lessSee more

## Access control requirements

Anyone can execute a SHOW CALLER GRANTS TO … command to list caller grants that have been granted to a specific executable owner.

Executing a SHOW CALLER GRANTS ON … command requires the following privilege:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any privilege | Specified object | You need at least one privilege on the object specified in the SHOW CALLER GRANTS command. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When executing a SHOW CALLER GRANTS ON … statement, different rows of the output can indicate different things. For example, one row
  could indicate a caller grant was granted directly on an object while another row indicates that the object was specified with an IN clause
  in the GRANT statement. For more information, see [List caller grants](/developer-guide/restricted-callers-rights#label-restricted-callers-rights-list).
- When a user executes SHOW CALLER GRANTS, the results only contain objects to which they have at least one privilege. For more information,
  see [Conditional output](/developer-guide/restricted-callers-rights#label-rcr-list-conditional-output).

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

## Examples

List caller grants that have been granted on the table `t1`.

> Copy code
>
> ```
> SHOW CALLER GRANTS ON TABLE t1;
> ```

List all of the caller grants that have been granted for the current account. This includes grants directly on the account
(GRANT CALLER … ON ACCOUNT) and grants to all objects in an account (GRANT INHERITED CALLER … IN ACCOUNT).

> Copy code
>
> ```
> SHOW CALLER GRANTS ON ACCOUNT;
> ```

List all of the caller grants that have been granted to the database role `db.owner_role`.

> Copy code
>
> ```
> SHOW CALLER GRANTS TO DATABASE ROLE db.owner_role;
> ```
