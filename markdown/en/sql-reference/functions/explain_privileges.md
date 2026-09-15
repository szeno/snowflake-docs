Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# EXPLAIN\_PRIVILEGES

Returns a JSON string that explains which privileges are required to execute a SQL statement.
This function analyzes the authorization requirements for a given SQL statement and returns
them in a structured format showing the required privileges, object types, and object names.

See also:
:   [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege),
    [SHOW GRANTS](/sql-reference/sql/show-grants)

## Syntax

Copy code

```
EXPLAIN_PRIVILEGES(
  statement => '<sql_statement>'
  [, missing_only => <boolean> ]
  [, for_role => '<role_name>' ])
```

## Arguments

`statement => 'sql_statement'`
:   A string containing the SQL statement to analyze. The statement is analyzed
    to determine which privileges are required to execute it.

`missing_only => boolean`
:   Boolean value that controls the output mode:

    - `false` - Returns all privileges required to execute the statement, regardless of
      whether the current user or specified role has them.
    - `true` — Returns only the privileges that are missing (not currently held by the current
      user or specified role). If all required privileges are present, returns
      `{"authorized": true}`.

    Default: `false`

`for_role => 'role_name'`
:   The name of a role to check privileges for. This argument is used only when
    `missing_only => true`. Returns all privileges missing for the role (and its granted roles)
    to execute the statement.

## Returns

The function returns a VARCHAR value containing a JSON object that describes the required privileges
in a hierarchical structure. The JSON can contain the following node types:

**Permission Node** — Represents a single privilege requirement:

Copy code

```
{
  "privilege": "<privilege_name>",
  "objectType": "<object_type>",
  "objectName": "<fully_qualified_object_name>"
}
```

- `privilege` — The name of the required privilege (for example, USAGE, SELECT, OWNERSHIP).
  The special value `<ANY>` indicates that any privilege on the object is sufficient.
- `objectType` — The type of object (for example, DATABASE, TABLE, SCHEMA, ACCOUNT).
- `objectName` — The fully qualified name of the object.

**AND Node** — All contained privileges are required:

Copy code

```
{
  "allOf": [
    /* ... permissions or nodes */
  ]
}
```

**OR Node** — At least one of the contained privileges is required:

Copy code

```
{
  "oneOf": [
    /* ... permissions or nodes */
  ]
}
```

**Decision Node** — Indicates authorization status

Copy code

```
{
  "authorized": true
}
```

- `authorized: true` — All required privileges are present.
- `authorized: false` — Statement cannot be authorized with privilege grants.

## Access control requirements

You must have privileges to refer to the object by name in the SQL statement. Most commonly, this requirement is satisfied by having at
least one privilege on the object. The RESOLVE ALL ON ACCOUNT privilege also meets this requirement.

## Usage notes

- `"authorized": true` means the current role, or the role specified in `for_role`, has
  sufficient privileges to execute the statement. The operation can still fail for other
  reasons; for example, [feature policies](/user-guide/feature-policies) can block it.
- The `statement` argument must be a constant expression. You cannot pass column values or other
  non-constant expressions.
- Multi-statement SQL is not supported. The function accepts only a single SQL statement.
- Some SQL statements are not supported for privilege analysis (for example, GRANT, REVOKE,
  USE ROLE, USE SECONDARY ROLES).
- Some SQL statements have privilege checks that are not supported for privilege analysis. These
  checks will be omitted from the output.
- Some indirect privilege checks are not supported for privilege analysis. These checks will be
  omitted from the output. For example RESOLVE ALL ON ACCOUNT is not included as an option to
  resolve a database.
- When an object cannot be resolved the function returns an error indicating that the statement
  requires access to all objects.
- The privilege `<ANY>` means any privilege on the object is sufficient (for example, for USAGE
  checks where OWNERSHIP would also suffice).

## Examples

The following examples call the EXPLAIN\_GRANTABLE\_PRIVILEGES function:

- [Explain privileges for a DESC command](#explain-privileges-for-a-desc-command)
- [Check only missing privileges](#check-only-missing-privileges)
- [Check missing privileges for a specific role](#check-missing-privileges-for-a-specific-role)

### Explain privileges for a DESC command

Show all privileges required to describe a schema:

Copy code

```
CALL EXPLAIN_PRIVILEGES(statement => 'DESC SCHEMA mydb.myschema');
```

Example output:

Copy code

```
{
  "allOf": [
    {
      "privilege": "<ANY>",
      "objectType": "DATABASE",
      "objectName": "MYDB"
    },
    {
      "privilege": "MONITOR",
      "objectType": "SCHEMA",
      "objectName": "MYDB.MYSCHEMA"
    }
  ]
}
```

This output indicates that you need any privilege on the database `MYDB` AND the `MONITOR` privilege
on the schema `MYDB.MYSCHEMA`.

### Check only missing privileges

Check what privileges are missing for the current user:

Copy code

```
CALL EXPLAIN_PRIVILEGES(
  statement => 'DROP TABLE mydb.myschema.mytable',
  missing_only => true);
```

If you have all required privileges, returns:

Copy code

```
{
  "authorized": true
}
```

If you’re missing privileges, returns only the missing ones:

Copy code

```
{
  "allOf": [
    {
      "privilege": "OWNERSHIP",
      "objectType": "TABLE",
      "objectName": "MYDB.MYSCHEMA.MYTABLE"
    }
  ]
}
```

### Check missing privileges for a specific role

Check what privileges a specific role is missing:

Copy code

```
CALL EXPLAIN_PRIVILEGES(
  statement => 'SELECT * FROM mydb.myschema.mytable',
  missing_only => true,
  for_role => 'analyst_role');
```

Determines whether the `analyst_role` (including privileges from its granted roles) has
the necessary privileges to execute the SELECT statement and, if not, returns the
missing privileges.
