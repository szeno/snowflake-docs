# EXECUTE NOTEBOOK

Executes the notebook outside the Notebook Editor. For example, you can run EXECUTE NOTEBOOK by itself from a worksheet, nest it within another
Snowflake executable such as a stored procedure or task, or use it in a third-party orchestrator.

The command runs the latest code from all cells in the notebook. Results are accessible from the Notebook Editor.

Note

EXECUTE NOTEBOOK also requires the QUERY\_WAREHOUSE parameter to be set, otherwise an error occurs. To set the QUERY\_WAREHOUSE parameter,
use the [ALTER NOTEBOOK](/sql-reference/sql/alter-notebook) command.

## Syntax

Copy code

```
EXECUTE NOTEBOOK <name>([ <parameter_string> [ , ... ] ]);
```

## Required parameters

`name`
:   Specifies the identifier (i.e. name) for the notebook; must be unique for the schema in which the notebook is created. Must be fully qualified
    if the notebook is not stored in the current `database.schema` you are operating in.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (for example, “My object”). Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`parameter_string`
:   Optionally pass in arguments to a notebook. In a Python cell in the notebook, you can access these arguments by using the `sys.argv` [variable](https://docs.python.org/3/library/sys.html#sys.argv).

    Only strings are supported; other data types (such as integers or booleans) are interpreted as NULL.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Notebook | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

When you run a notebook using the EXECUTE NOTEBOOK command:

- Python cells are executed on the compute pool defined by the RUNTIME parameter.
- SQL and Snowpark queries are executed using the virtual warehouse specified in the WAREHOUSE parameter.
- Snowflake doesn’t support embedding the `EXECUTE NOTEBOOK` command in a task that is configured to [EXECUTE AS USER](/user-guide/tasks-intro#label-user-based-security-for-tasks).
  You will not see an error message when creating such a task, but when the task is executed, it will fail.
- When you execute a notebook that uses a compute pool, the Python code runs on the compute pool. However, you might see activity in
  **Query History** showing that a warehouse was used to run the EXECUTE NOTEBOOK command. This is expected behavior. The warehouse is
  used briefly to initialize the notebook execution environment, but it does not consume any warehouse credits. All code execution is
  handled by the compute pool.

## Example

The following example triggers the default version of the specified notebook without passing in any arguments:

Copy code

```
EXECUTE NOTEBOOK MY_DB.PUBLIC.MY_NOTEBOOK();
```

## Pass parameters to a notebook

You can optionally pass in arguments when running a notebook. In Python cells, you can access these arguments by using the `sys.argv` variable, which is [a built-in Python list that holds command-line arguments](https://docs.python.org/3/library/sys.html#sys.argv).

You can use arguments to customize notebook behavior; for example, you can pass in input values, specify a target
environment, or adjust execution logic based on these arguments.

### Example

Copy code

```
EXECUTE NOTEBOOK MY_DATABASE.PUBLIC.MY_NOTEBOOK(
  'parameter_string a,b,c,d',
  'target_database=PROD_DB'
);
```

In a Python cell in the notebook, you can access each argument as a string in the `sys.argv` list.

To learn how to access and use these arguments from a notebook (including how to parse lists or extract key-value pairs), see [Develop and run code in Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-develop-run).
