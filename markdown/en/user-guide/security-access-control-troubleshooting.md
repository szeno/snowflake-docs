# Troubleshooting access control issues

If a SQL statement fails because the role being used to run the query lacks the required access control privileges, you can use the
[EXPLAIN\_PRIVILEGES](/sql-reference/functions/explain_privileges) function to determine exactly which privileges are missing.

## Troubleshooting as an administrator

An administrator who has privileges on all objects in Snowflake can call the EXPLAIN\_PRIVILEGES function on any SQL statement.

Tip

If you want someone who doesn’t have privileges on objects to be able to diagnose access control issues using EXPLAIN\_PRIVILEGES, grant them the RESOLVE ALL ON ACCOUNT privilege.

**Example: List all privileges needed to run a SQL statement**

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

**Example: List the missing privileges for a specific role**

The following call determines whether the `analyst_role` (including privileges from its granted roles) has
the necessary privileges to execute the SELECT statement and, if not, returns the
missing privileges.

Copy code

```
CALL EXPLAIN_PRIVILEGES(
  statement => 'SELECT * FROM mydb.myschema.mytable',
  missing_only => true,
  for_role => 'analyst_role');
```

## Troubleshooting your own query

You must have at least one privilege on the objects referenced in your query to call the EXPLAIN\_PRIVILEGES function. If those privileges on the object aren’t enough to successfully run your query, call the EXPLAIN\_PRIVILEGES function with the `missing_only`
argument set to `true` to determine the additional privileges that are required.

For example, if you have privileges on the `mydb`, `myschema`, and `mytable` objects, but your query is still failing because of access control issues, run the following command:

Copy code

```
CALL EXPLAIN_PRIVILEGES(
  statement => 'SELECT * FROM mydb.myschema.mytable',
  missing_only => true);
```

If your current role is missing privileges, the function returns the specific privileges you need. For example:

Copy code

```
{
  "allOf": [
    {
      "privilege": "SELECT",
      "objectType": "TABLE",
      "objectName": "MYDB.MYSCHEMA.MYTABLE"
    }
  ]
}
```
