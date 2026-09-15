# EXECUTE IMMEDIATE FROM

EXECUTE IMMEDIATE FROM executes the SQL statements specified in a file in a stage. The file can contain
SQL statements or [Snowflake Scripting blocks](/developer-guide/snowflake-scripting/blocks). The statements must be syntactically
correct SQL statements.

You can use the EXECUTE IMMEDIATE FROM command to execute the statements in a file from any Snowflake session.

This feature provides a mechanism to control the deployment and management of your Snowflake objects and code. For example, you can execute
a stored script to create a standard Snowflake environment for all your accounts. The configuration script might include statements
that create users, roles, databases, and schemas for every new account.

## Jinja2 templating

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

EXECUTE IMMEDIATE FROM can also execute a template file using the Jinja2 templating language.
A template can contain variables and expressions, enabling the use of loops, conditionals, variable substitution, macros, and more.
Templates can also include other templates and can import macros defined in other files located on a stage.

For more information about the templating language, see the [Jinja2 documentation](https://jinja.palletsprojects.com/).

The template file to be executed must be:

- A syntactically valid Jinja2 template.
- Located in a stage or [Git repository clone](/developer-guide/git/git-overview).
- Able to render syntactically valid SQL statements.

Templating enables more flexible control structures and parameterization using environment variables. For example, you can use
a template to dynamically choose the deployment target of the objects defined in the script. To use a template to render a
SQL script, use the [templating directive](#label-execute-immediate-from-templating-directive) or add a
[USING clause](/sql-reference/sql/execute-immediate-from#label-execute-immediate-from-using-clause) with at least one template variable.

### Templating directive

You can use either one of the two templating directives.

The recommended directive uses valid SQL syntax:

Copy code

```
--!jinja
```

Optionally, you can use the alternative directive:

Copy code

```
#!jinja
```

Note

Only a byte order mark and up to 10 whitespace characters (newlines, tabs, spaces) may be placed in front of the directive.
Any characters that come after the directive on the same line will be ignored.

### Using content from staged files in a template

A template can load other staged files either directly through the
[SnowflakeFile API](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/files)
or through Jinja2’s [include](https://jinja.palletsprojects.com/en/stable/templates/#include),
[import](https://jinja.palletsprojects.com/en/stable/templates/#import), and
[inheritance](https://jinja.palletsprojects.com/en/stable/templates/#template-inheritance) features.

Files can be referenced by absolute paths:

Copy code

```
{% include "@my_stage/path/to/my_template" %}
{% import "@my_stage/path/to/my_template" as my_template %}
{% extends "@my_stage/path/to/my_template" %}
{{ SnowflakeFile.open("@my_stage/path/to/my_template", 'r', require_scoped_url = False).read() }}
```

Include, import, and extends also support relative paths while the SnowflakeFile API supports scoped Snowflake file URLs:

Copy code

```
{% include "my_template" %}
{% import "../my_template" as my_template %}
{% extends "/path/to/my_template" %}
```

See also:
:   [EXECUTE IMMEDIATE](/sql-reference/sql/execute-immediate)

## Syntax

Copy code

```
EXECUTE IMMEDIATE
  FROM { absoluteFilePath | relativeFilePath }
  [ USING ( <key> => <value> [ , <key> => <value> [ , ... ] ]  )  ]
  [ DRY_RUN = { TRUE | FALSE } ]
```

Where:

> Copy code
>
> ```
> absoluteFilePath ::=
>    @[ <namespace>. ]<stage_name>/<path>/<filename>
> ```
>
> Copy code
>
> ```
> relativeFilePath ::=
>   '[ / | ./ | ../ ]<path>/<filename>'
> ```

## Required parameters

### Absolute file path (`absoluteFilePath`)

`namespace`
:   Database and/or schema in which the internal or external stage resides, in the form of `database_name.schema_name`
    or `schema_name`. The namespace is optional if a database and schema are currently in use for the user session; otherwise,
    it is required.

`stage_name`
:   Name of the internal or external stage.

`path`
:   Case-sensitive path to the file in the stage.

`filename`
:   Name of the file to execute. It must contain syntactically correct and valid SQL statements. Each statement must be
    separated by a semicolon.

### Relative file path (`relativeFilePath`)

`path`
:   Case-sensitive relative path to the file in the stage. Relative paths support established conventions such as a leading `/`
    to indicate the root of a stage’s file system, `./` to refer to the current directory (the directory the parent file is
    located in) and `../` to refer to the parent directory. For more information, see [Usage notes](#label-execute-immediate-from-usage-notes).

`filename`
:   Name of the file to execute. It must contain syntactically correct and valid SQL statements. Each statement must be
    separated by a semicolon.

## Optional parameters

`USING ( <key> => <value> [ , <key> => <value> [ , ... ] ] )`

> [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
>
> Available to all accounts.
>
> Allows you to pass one or more key-value pairs that can be used to parameterize template expansion. The key-value pairs
> must form a comma-separated list.
>
> When the USING clause is present, the file is first [rendered as a Jinja2 template](#label-execute-immediate-from-templating)
> before being executed as a SQL script.
>
> Where:
>
> > - `key` is the name of the template variable. The template variable name can optionally be enclosed in double quotes
> >   (`"`).
> > - `value` is the value to assign to the variable in the template. String values must be enclosed in `'` or
> >   `$$`. For an example, see [Templating usage notes](#templating-usage-notes).

`DRY_RUN = { TRUE | FALSE }`

> [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
>
> Available to all accounts.
>
> Specifies whether to preview the [rendered file](#label-execute-immediate-from-templating) without executing it as a SQL script.
>
> - `TRUE` returns the rendered file contents without executing the SQL statements.
> - `FALSE` renders SQL statements from the template and executes those statements.
>
> Default: `FALSE`

## Returns

EXECUTE IMMEDIATE FROM returns:

- The result of the last statement in the file if all statements are successfully executed.
- The error message, if any statement in the file failed.

  If there is an error in any statement in the file, the EXECUTE IMMEDIATE FROM command fails and returns the error message
  of the failed statement.

  Note

  If the EXECUTE IMMEDIATE FROM command fails and returns an error message, any statements in the file prior to the failed statement
  have successfully completed.

## Access control requirements

- The [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute the EXECUTE IMMEDIATE FROM command must have the
  USAGE (external stage) or READ (internal stage) privilege on the stage where the file is located.

- The role used to execute the file can only execute the statements in the file for which it has privileges.
  For example, if there is a CREATE TABLE statement in the file, the role must have the
  [necessary privileges to create a table](/sql-reference/sql/create-table#label-create-table-access-control-requirements) in the account or the statement fails.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The SQL statements in a file to be executed can include EXECUTE IMMEDIATE FROM statements:

  - Nested EXECUTE IMMEDIATE FROM statements *can* use [relative file paths](/sql-reference/sql/execute-immediate-from#label-execute-immediate-from-relative-path).

    Relative paths are evaluated in respect to the stage and file path of the parent file. If the relative file path starts with
    `/`, the path starts at the root directory of the stage containing the parent file.

    For an example, see [Examples](#label-execute-immediate-from-examples).
  - Relative file paths must be enclosed in single quotes (`'`) or `$$`.
  - The maximum execution depth for nested files is 5.
- Absolute file paths can optionally be enclosed in single quotes (`'`) or `$$`.
- The file to be executed cannot be larger than 10MB in size.
- The file to be executed must be encoded in [UTF-8](https://en.wikipedia.org/wiki/UTF-8).
- The file to be executed must be uncompressed. If you use the [PUT](/sql-reference/sql/put) command to upload a file to an internal
  stage, you must explicitly set the [AUTO\_COMPRESS parameter](/sql-reference/sql/put#label-put-parameter-auto-compress) to FALSE.

  For example, upload `my_file.sql` to `my_stage`:

  Copy code

  ```
  PUT file://~/sql/scripts/my_file.sql @my_stage/scripts/
    AUTO_COMPRESS=FALSE;
  ```
- The execution of all files in a directory is not supported. For example, `EXECUTE IMMEDIATE FROM @stage_name/scripts/`
  results in an error.

## Templating usage notes

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

- Variable names in templates are case-sensitive.
- The template variable name can be optionally enclosed in double quotes. Enclosing the variable name can be useful if any
  [reserved keywords](/sql-reference/reserved-keywords) are used as variable names.
- The following parameter types are supported in the USING clause:

  - String. Must be enclosed by `'` or `$$`. For example, `USING (a => 'a', b => $$b$$)`.
  - Number (decimal and integer). For example, `USING (a => 1, b => -1.23)`.
  - Boolean. For example, `USING (a => TRUE, b => FALSE)`.
  - NULL. For example, `USING (a => NULL)`.

    Note

    The Jinja2 templating engine interprets a NULL value as the Python NoneType type.
  - [Session variables](/sql-reference/session-variables). For example, `USING (a => $var)`. Only session variables holding
    values of supported data types are allowed.
  - [Bind variables](/sql-reference/bind-variables#label-bind-variables-with-snowflake-scripting). For example, `USING (a => :var)`. Only bind variables
    holding values of supported data types are allowed. You can use bind variables to pass stored procedure arguments to a template.
- Files in Snowflake Git repositories or in Snowflake Native Apps cannot be accessed from the template.
- The maximum result size for template rendering is 100,000 bytes.
- Templates are rendered using the Jinja2 version 3.1.6 templating engine.

## Troubleshooting EXECUTE IMMEDIATE FROM errors

This section contains some common errors that result from an EXECUTE IMMEDIATE FROM statement and how you can resolve them.

- [File errors](#label-execute-immediate-from-file-errors)
- [Stage errors](#label-execute-immediate-from-stage-errors)
- [Access control errors](#label-execute-immediate-from-privilege-errors)
- [Templating errors](#label-execute-immediate-from-templating-errors)

### File errors

|  |  |
| --- | --- |
| Error | ``` 001501 (02000): File '<directory_name>' not found in stage '<stage_name>'. ``` |
| Cause | There are multiple causes for this error:   - The file does not exist. - The file name is the root of a directory. For example `@stage_name/scripts/`. |
| Solution | Verify the name of the file and confirm the file exists. Executing all the files in a directory is not supported. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` 001503 (42601): Relative file references like '<filename.sql>' cannot be used in top-level EXECUTE IMMEDIATE calls. ``` |
| Cause | The statement was executed using a relative file path outside of a file execution. |
| Solution | A relative file path can only be used in EXECUTE IMMEDIATE FROM statements in a file. Use the [absolute file path](#label-execute-immediate-from-absolute-filepath) for the file. For more information, see [Usage notes](#label-execute-immediate-from-usage-notes). |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` 001003 (42000): SQL compilation error: syntax error line <n> at position <m> unexpected '<string>'. ``` |
| Cause | The file contains SQL syntax errors. |
| Solution | Fix the syntax errors in the file and reupload the file to the stage. |

Expand

Show lessSee more

### Stage errors

|  |  |
| --- | --- |
| Error | ``` 002003 (02000): SQL compilation error: Stage '<stage_name>' does not exist or not authorized. ``` |
| Cause | The stage does not exist or you do not have access to the stage. |
| Solution | - Verify the name of the stage and confirm the stage exists. - Execute the statement using a role that has the required privileges to access the stage. For more information, see   [Access control requirements](#label-execute-immediate-from-access-control-requirements). |

Expand

Show lessSee more

### Access control errors

|  |  |
| --- | --- |
| Error | ``` 003001 (42501): Uncaught exception of type 'STATEMENT_ERROR' in file <file_name> on line <n> at position <m>: SQL access control error: Insufficient privileges to operate on schema '<schema_name>' ``` |
| Cause | The role used to execute the statement does not have the privileges required to execute some or all of the statements in the file. |
| Solution | Use a role that has the appropriate privileges to execute the statements in the file. For more information, see [Access control requirements](#label-execute-immediate-from-access-control-requirements). |

Expand

Show lessSee more

See also: [Stage errors](#label-execute-immediate-from-stage-errors).

### Templating errors

|  |  |
| --- | --- |
| Error | ``` 001003 (42000): SQL compilation error: syntax error line [n] at position [m] unexpected '{'. ``` |
| Cause | The file contains templating constructs (for example, `{{ table_name }}`) but is not rendered using the templating engine. If the template is not rendered, the lines of text in the template are executed as SQL statements. The templating constructs in the file are likely to result in SQL syntax errors. |
| Solution | Add a [templating directive](#label-execute-immediate-from-templating-directive) or re-execute the statement with the [USING clause](/sql-reference/sql/execute-immediate-from#label-execute-immediate-from-using-clause) and specify at least one template variable. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` 000005 (XX000): Python Interpreter Error: jinja2.exceptions.UndefinedError: '<key>' is undefined in template processing ``` |
| Cause | If any variables used in the template are left unspecified in the USING clause, an error occurs. |
| Solution | Verify the names and number of variables in the template and update the USING clause to include values for all template variables. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` 001510 (42601): Unable to use value of template variable '<key>' ``` |
| Cause | The value for the variable `key` is an unsupported type. |
| Solution | Verify that you are using a supported parameter type for the template variable value. For more information, see the [Templating usage notes](#label-execute-immediate-from-templating-notes). |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` 001518 (42601): Size of expanded template exceeds limit of 100,000 bytes. ``` |
| Cause | The size of the rendered template exceeds the current limit. |
| Solution | Split your templated file into multiple smaller templates and add a new script to execute them sequentially, while passing down template variables to the nested scripts. |

Expand

Show lessSee more

## Examples

### Basic example

This example executes the file `create-inventory.sql` located in stage `my_stage`.

1. Create a file named `create-inventory.sql` with the following statements:

   Copy code

   ```
   CREATE OR REPLACE TABLE my_inventory(
     sku VARCHAR,
     price NUMBER
   );

   EXECUTE IMMEDIATE FROM './insert-inventory.sql';

   SELECT sku, price
     FROM my_inventory
     ORDER BY price DESC;
   ```
2. Create a file named `insert-inventory.sql` with the following statements:

   Copy code

   ```
   INSERT INTO my_inventory
     VALUES ('XYZ12345', 10.00),
         ('XYZ81974', 50.00),
         ('XYZ34985', 30.00),
         ('XYZ15324', 15.00);
   ```
3. Create an internal stage `my_stage`:

   Copy code

   ```
   CREATE STAGE my_stage;
   ```
4. Upload both local files to the stage using the [PUT](/sql-reference/sql/put) command:

   Copy code

   ```
   PUT file://~/sql/scripts/create-inventory.sql @my_stage/scripts/
     AUTO_COMPRESS=FALSE;

   PUT file://~/sql/scripts/insert-inventory.sql @my_stage/scripts/
     AUTO_COMPRESS=FALSE;
   ```
5. Execute the `create-inventory.sql` script located in `my_stage`:

   Copy code

   ```
   EXECUTE IMMEDIATE FROM @my_stage/scripts/create-inventory.sql;
   ```

   Returns:

   ```
   +----------+-------+
   | SKU      | PRICE |
   |----------+-------|
   | XYZ81974 |    50 |
   | XYZ34985 |    30 |
   | XYZ15324 |    15 |
   | XYZ12345 |    10 |
   +----------+-------+
   ```

### A simple template example

1. Create a template file `setup.sql` with two variables and the templating directive:

   Copy code

   ```
   --!jinja

   CREATE SCHEMA {{env}};

   CREATE TABLE RAW (COL OBJECT)
    DATA_RETENTION_TIME_IN_DAYS = {{retention_time}};
   ```
2. Create a stage — *optional* if you already have a stage to which you can upload files.

   For example, create an internal stage in Snowflake:

   Copy code

   ```
   CREATE STAGE my_stage;
   ```
3. Upload the file to your stage.

   For example, use the [PUT](/sql-reference/sql/put) command from your local environment to upload file `setup.sql`
   to stage `my_stage`:

   Copy code

   ```
   PUT file://path/to/setup.sql @my_stage/scripts/
     AUTO_COMPRESS=FALSE;
   ```
4. Execute the file `setup.sql`:

   Copy code

   ```
   EXECUTE IMMEDIATE FROM @my_stage/scripts/setup.sql
    USING (env=>'dev', retention_time=>0);
   ```

### A template example with macros, conditionals, loops, and imports

1. Create a template file containing a macro definition.

   For example, create a file `macros.jinja` in your local environment:

   Copy code

   ```
   {%- macro get_environments(deployment_type) -%}
     {%- if deployment_type == 'prod' -%}
    {{ "prod1,prod2" }}
     {%- else -%}
    {{ "dev,qa,staging" }}
     {%- endif -%}
   {%- endmacro -%}
   ```
2. Create a template file and add the templating directive (`--!jinja2`) to the top of the file.

   After the templating directive, add an `import` statement to import the macro defined in the
   file that you created in the previous step.
   For example, create a file `setup-env.sql` in your local environment:

   Copy code

   ```
   --!jinja2
   {% from "macros.jinja" import get_environments %}

   {%- set environments = get_environments(DEPLOYMENT_TYPE).split(",") -%}

   {%- for environment in environments -%}
     CREATE DATABASE {{ environment }}_db;
     USE DATABASE {{ environment }}_db;
     CREATE TABLE {{ environment }}_orders (
    id NUMBER,
    item VARCHAR,
    quantity NUMBER);
     CREATE TABLE {{ environment }}_customers (
    id NUMBER,
    name VARCHAR);
   {% endfor %}
   ```
3. Create a stage — *optional* if you already have a stage to which you can upload files.

   For example, create an internal stage in Snowflake:

   Copy code

   ```
   CREATE STAGE my_stage;
   ```
4. Upload the file to your stage.

   For example, use the [PUT](/sql-reference/sql/put) command from your local environment to upload the files
   `setup-env.sql` and `macros.jinja` to the stage `my_stage`:

   Copy code

   ```
   PUT file://path/to/setup-env.sql @my_stage/scripts/
     AUTO_COMPRESS=FALSE;
   PUT file://path/to/macros.jinja @my_stage/scripts/
     AUTO_COMPRESS=FALSE;
   ```
5. Preview the SQL statements rendered by the template to check for any problems with your Jinja2 code:

   Copy code

   ```
   EXECUTE IMMEDIATE FROM @my_stage/scripts/setup-env.sql
     USING (DEPLOYMENT_TYPE => 'prod') DRY_RUN = TRUE;
   ```

   Returns:

   ```
   +----------------------------------+
   | rendered file contents           |
   |----------------------------------|
   | --!jinja2                        |
   | CREATE DATABASE prod1_db;        |
   |   USE DATABASE prod1_db;         |
   |   CREATE TABLE prod1_orders (    |
   |     id NUMBER,                   |
   |     item VARCHAR,                |
   |     quantity NUMBER);            |
   |   CREATE TABLE prod1_customers ( |
   |     id NUMBER,                   |
   |     name VARCHAR);               |
   | CREATE DATABASE prod2_db;        |
   |   USE DATABASE prod2_db;         |
   |   CREATE TABLE prod2_orders (    |
   |     id NUMBER,                   |
   |     item VARCHAR,                |
   |     quantity NUMBER);            |
   |   CREATE TABLE prod2_customers ( |
   |     id NUMBER,                   |
   |     name VARCHAR);               |
   |                                  |
   +----------------------------------+
   ```
6. Execute the file `setup-env.sql`:

   Copy code

   ```
   EXECUTE IMMEDIATE FROM @my_stage/scripts/setup-env.sql
     USING (DEPLOYMENT_TYPE => 'prod');
   ```
