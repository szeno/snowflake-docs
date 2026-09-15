# Managing Snowflake objects

The `snow object` commands provide you with a convenient way of managing most Snowflake objects, such as stages, Snowpark functions, or Streamlit apps. Instead of using separate commands for each type of object, you can use these commands to perform common tasks, including the following:

- [Create an object of a specific type](#label-snowcli-object-create)
- [List available objects of a specified type](#label-snowcli-object-list).
- [Display the description of an object](#label-snowcli-object-describe).
- [Delete an object](#label-snowcli-object-drop).

To see a list of supported types use the `--help` option for any of the `snow object` commands, such as the following:

Copy code

```
snow object list --help
```

```
Usage: snow object list [OPTIONS] OBJECT_TYPE

Lists all available Snowflake objects of given type.
Supported types: compute-pool, database, function, image-repository, integration, network-rule,
procedure, role, schema, secret, service, stage, stream, streamlit, table, task,
user, view, warehouse

...
```

The object subcommands let you perform common operations, while leaving service-specific commands groups dedicated to service-specific operations.

## Create an object of a specific type

The `snow object create` command creates a specified object based on the definition provided, using the following syntax:

Copy code

```
snow object create TYPE ([OBJECT_ATTRIBUTES]|[--json {OBJECT_DEFINITION}])
```

where:

- `TYPE` is a Snowflake object type:
  - `account`
  - `catalog-integration`
  - `compute-pool`
  - `database`
  - `database-role`
  - `dynamic-table`
  - `event-table`
  - `external-volume`
  - `function`
  - `image-repository`
  - `managed-account`
  - `network-policy`
  - `notebook`
  - `notification-integration`
  - `pipe`
  - `procedure`
  - `role`
  - `schema`
  - `service`
  - `stage`
  - `stream`
  - `table`
  - `task`
  - `user-defined-function`
  - `view`
  - `warehouse`

- `OBJECT_ATTRIBUTES` contains the object definition in the form of a list of `<key>=<value>` pairs, such as:

  Copy code

  ```
  snow object create database name=my_db comment="Created with Snowflake CLI"
  ```
- `--json {OBJECT_DEFINITION}` contains the object definition in JSON, such as:

  Copy code

  ```
  snow object create database --json '{"name":"my_db", "comment":"Created with Snowflake CLI"}'
  ```

Note

The following object types require a database to be identified in the connection configuration, such as `config.toml`, or passed to the command using the `--database` option.

- image-repository
- schema
- service
- table
- task

To create a database object using the `option-attributes` parameter:

Copy code

```
snow object create database name=my_db comment='Created with Snowflake CLI'
```

To create a table object using the `option-attributes` parameter:

Copy code

```
snow object create table name=my_table columns='[{"name":"col1","datatype":"number", "nullable":false}]' constraints='[{"name":"prim_key", "column_names":["col1"], "constraint_type":"PRIMARY KEY"}]' --database my_db --schema public
```

To create a database using the `--json object-definition` option:

Copy code

```
snow object create database --json '{"name":"my_db", "comment":"Created with Snowflake CLI"}'
```

To create a table using the `--json object-definition` option:

Copy code

```
snow object create table --json "$(cat table.json)" --database my_db
```

where `table.json` contains the following:

Copy code

```
{
  "name": "my_table",
  "columns": [
    {
      "name": "col1",
      "datatype": "number",
      "nullable": false
    }
  ],
  "constraints": [
    {
      "name": "prim_key",
      "column_names": ["col1"],
      "constraint_type": "PRIMARY KEY"
    }
  ]
}
```

## List all objects of a specific type

The `snow object list` command lists all objects of given type available with your permissions.

Copy code

```
snow object list TYPE
```

where `TYPE` is the type of the object. Use `snow object list --help` for the full list of supported types.

To list all role objects, enter the following command:

Copy code

```
snow object list role
```

```
+--------------------------------------------------------------------------------------------------------------------------------+
|            |            |            |            | is_inherit | assigned_t | granted_to | granted_ro |            |           |
| created_on | name       | is_default | is_current | ed         | o_users    | _roles     | les        | owner      | comment   |
|------------+------------+------------+------------+------------+------------+------------+------------+------------+-----------|
| 2023-07-24 | ACCOUNTADM | N          | N          | N          | 2          | 0          | 2          |            | Account   |
| 06:05:49-0 | IN         |            |            |            |            |            |            |            | administr |
| 7:00       |            |            |            |            |            |            |            |            | ator can  |
|            |            |            |            |            |            |            |            |            | manage    |
|            |            |            |            |            |            |            |            |            | all       |
|            |            |            |            |            |            |            |            |            | aspects   |
|            |            |            |            |            |            |            |            |            | of the    |
|            |            |            |            |            |            |            |            |            | account.  |
| 2023-07-24 | PUBLIC     | N          | N          | Y          | 0          | 0          | 0          |            | Public    |
| 06:05:48.9 |            |            |            |            |            |            |            |            | role is   |
| 56000-07:0 |            |            |            |            |            |            |            |            | automatic |
| 0          |            |            |            |            |            |            |            |            | ally      |
|            |            |            |            |            |            |            |            |            | available |
|            |            |            |            |            |            |            |            |            | to every  |
|            |            |            |            |            |            |            |            |            | user in   |
|            |            |            |            |            |            |            |            |            | the       |
|            |            |            |            |            |            |            |            |            | account.  |
| 2023-07-24 | SYSADMIN   | N          | N          | N          | 0          | 1          | 0          |            | System    |
| 06:05:49.0 |            |            |            |            |            |            |            |            | administr |
| 33000-07:0 |            |            |            |            |            |            |            |            | ator can  |
| 0          |            |            |            |            |            |            |            |            | create    |
|            |            |            |            |            |            |            |            |            | and       |
|            |            |            |            |            |            |            |            |            | manage    |
|            |            |            |            |            |            |            |            |            | databases |
|            |            |            |            |            |            |            |            |            | and       |
|            |            |            |            |            |            |            |            |            | warehouse |
|            |            |            |            |            |            |            |            |            | s.        |
| 2023-07-24 | USERADMIN  | N          | N          | N          | 0          | 1          | 0          |            | User      |
| 06:05:49.0 |            |            |            |            |            |            |            |            | administr |
| 45000-07:0 |            |            |            |            |            |            |            |            | ator can  |
| 0          |            |            |            |            |            |            |            |            | create    |
|            |            |            |            |            |            |            |            |            | and       |
|            |            |            |            |            |            |            |            |            | manage    |
|            |            |            |            |            |            |            |            |            | users and |
|            |            |            |            |            |            |            |            |            | roles     |
+--------------------------------------------------------------------------------------------------------------------------------+
```

You can also use the `--like [-l] <pattern>` to filter objects by name using a SQL LIKE pattern. For example, `list function --like "my%"` lists all functions that begin with **my**. For more information about SQL patterns syntax, see [SQL LIKE Keyword](https://www.w3schools.com/sql/sql_ref_like.asp).

To list only role objects that begin with the string, **public**, enter the following command:

Copy code

```
snow object list role --like public%
```

```
show roles like 'public%'
+-------------------------------------------------------------------------------
| created_on                       | name        | is_default | is_current | ...
|----------------------------------+-------------+------------+------------+----
| 2023-02-01 15:25:04.105000-08:00 | PUBLIC      | N          | N          | ...
| 2024-01-15 12:55:05.840000-08:00 | PUBLIC_TEST | N          | N          | ...
+-------------------------------------------------------------------------------
```

## Display the description for an object of a specified type

The `snow object describe` command provides a description of an object of given type.

Copy code

```
snow object describe TYPE IDENTIFIER
```

where:

- `TYPE` is the type of the object. Use `snow object describe --help` for the full list of supported types.
- `IDENTIFIER` is the name of the object. For procedures and functions, the identifier must specify arguments types, such as `"hello(int,string)"`.

To describe a function object, enter a command similar to the following:

Copy code

```
snow object describe function "hello_function(string)"
```

```
describe function hello_function(string)
+---------------------------------------------------------------------
| property           | value
|--------------------+------------------------------------------------
| signature          | (NAME VARCHAR)
| returns            | VARCHAR(16777216)
| language           | PYTHON
| null handling      | CALLED ON NULL INPUT
| volatility         | VOLATILE
| body               | None
| imports            |
| handler            | functions.hello_function
| runtime_version    | 3.9
| packages           | ['snowflake-snowpark-python']
| installed_packages | ['_libgcc_mutex==0.1','_openmp_mutex==5.1',...
+---------------------------------------------------------------------
```

## Delete an object of a specified type

The `snow object drop` command deletes a Snowflake object of given name and type.

Copy code

```
snow object drop TYPE IDENTIFIER
```

where:

- `TYPE` is the type of the object. Use `snow object drop --help` for the full list of supported types.
- `IDENTIFIER` is the name of the object. For procedures and functions, the identifier must specify arguments types, such as `"hello(int,string)"`.

To drop a procedure, enter a commands similar to the following:

Copy code

```
snow object drop procedure "test_procedure()"
```

```
drop procedure test_procedure()
+--------------------------------------+
| status                               |
|--------------------------------------|
| TEST_PROCEDURE successfully dropped. |
+--------------------------------------+
```
