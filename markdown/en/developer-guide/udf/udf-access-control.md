# Granting privileges for user-defined functions

This topic lists the minimum privileges required on objects to perform specific SQL actions with a UDF or UDTF.

## Granting privileges for UDFs and UDTFs

To perform SQL actions on a UDF or UDTF, the person performing the action must have been assigned a role that has been granted the required
privileges. These SQL actions include:

- Creating the function, such as with [CREATE FUNCTION](/sql-reference/sql/create-function) or with the
  [Snowpark API](/developer-guide/snowpark/index).
- Owning the function in order to delete, alter, and manage access to the function, whether through SQL or the Snowpark API.
- Calling the function, whether with SQL or the Snowpark API.

The role must be assigned privileges on objects related to the function, including the database and schema, and (if required) a
stage that holds function dependencies.

To grant privileges on an object to a role, use a [GRANT](/sql-reference/sql/grant-privilege) statement.

Code in the following example grants to `my_role` the USAGE privilege on the function `my_java_udf`.

Copy code

```
GRANT USAGE ON FUNCTION my_java_udf(number, number) TO my_role;
```

### Creating UDFs or UDTFs

Creating, managing, and executing a UDF or UDTF requires a role with a minimum of the following privileges:

| Object | Privileges | Notes |
| --- | --- | --- |
| Database | USAGE |  |
| Schema | USAGE, CREATE FUNCTION |  |
| Stage | USAGE (external stage) or READ (internal stage) | Required if the function depends on or reads from files on a stage. This would include the following staged files:   - File containing handler code for a UDF. For more information about staged and in-line handlers, see   [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged). - Libraries that the handler code requires as dependencies, including JAR files, Python modules, .zip files, and so on. For more   information, see [Making dependencies available to your code](/developer-guide/upload-dependencies). - Files containing content read by code in the handler. This includes unstructured data processed by the handler. |

Expand

Show lessSee more

### Owning UDFs or UDTFs

After a UDF or UDTF is created, the function owner (that is, a person with the role that has the OWNERSHIP privilege on the function)
must have a minimum of the following privileges:

| Object | Privilege | Notes |
| --- | --- | --- |
| Database | USAGE |  |
| Schema | USAGE |  |
| Stage | USAGE (external stage) or READ (internal stage) | Required if the function depends on or reads from files on a stage. This would include the following staged files:   - File containing handler code for a UDF. For more information about staged and in-line handlers, see   [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged). - Libraries that the handler code requires as dependencies, including JAR files, Python modules, .zip files, and so on. For more   information, see [Making dependencies available to your code](/developer-guide/upload-dependencies). - Files containing content read by code in the handler. This includes unstructured data processed by the handler. |
| Function | OWNERSHIP |  |

Expand

Show lessSee more

### Calling UDFs or UDTFs

A role that calls a UDF or UDTF must have a minimum of the following privileges:

| Object | Privilege | Notes |
| --- | --- | --- |
| Database | USAGE |  |
| Schema | USAGE | Schema that contains the schema-level objects in this table. If the objects are contained in multiple schemas, the USAGE privilege is required on each. |
| Stage | USAGE (external stage) or READ (internal stage) | Required if the function depends on or reads from files on a stage. This would include the following staged files:   - File containing handler code for a UDF. For more information about staged and in-line handlers, see   [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged). - Libraries that the handler code requires as dependencies, including JAR files, Python modules, .zip files, and so on. For more   information, see [Making dependencies available to your code](/developer-guide/upload-dependencies). - Files containing content read by code in the handler. This includes unstructured data processed by the handler. |
| Function | USAGE | Required when anyone other than the function’s owner will call the function. USAGE on the function must be granted to a role that is assigned to a person who will call the function. |

Expand

Show lessSee more
