# SQL variables

You can define and use SQL variables in sessions in Snowflake.

## Overview

Snowflake supports SQL variables declared by the user. They have many uses, such as storing application-specific environment settings.

### Variable identifiers

SQL variables are globally identified using case-insensitive names.

### Variable DDL

Snowflake provides the following DDL commands for using SQL variables:

- [SET](/sql-reference/sql/set)
- [UNSET](/sql-reference/sql/unset)
- [SHOW VARIABLES](/sql-reference/sql/show-variables)

## Initializing variables

You can set variables by executing the SQL statement [SET](/sql-reference/sql/set) or by setting the variables in the connection
string when you connect to Snowflake.

The size of string or binary variables is limited to 16KB.

### Using SQL to initialize variables in a session

You can initialize variables in SQL using the [SET](/sql-reference/sql/set) command. The data type of the variable is derived from the
data type of the result of the evaluated expression. The following examples initialize variables:

Copy code

```
SET my_variable1 = 10;
SET my_variable2 = 'example';
```

You can initialize variables by using queries that return a single result. The following examples initialize variables by
using queries:

Copy code

```
SET cust_last_name = (SELECT lname FROM customers WHERE customer_id=100);
SET timestamp_variable = (SELECT CURRENT_TIMESTAMP());
```

You can initialize multiple variables in the same statement, thereby reducing the number of round-trip communications with the server.
The following examples initialize multiple variables:

Copy code

```
SET (var1, var2, var3) = (10, 20, 30);
SET (current_user, current_warehouse) = ((SELECT CURRENT_USER()), (SELECT CURRENT_WAREHOUSE()));
```

### Setting variables on connection

In addition to using [SET](/sql-reference/sql/set) to set variables within a session, you can pass variables as arguments in the connection
string used to initialize a session in Snowflake. This option is especially useful when using tools where the specification of the connection string
is the only customization possible.

For example, using the Snowflake JDBC driver, you can set additional connection properties that are interpreted as parameters.
The JDBC API requires SQL variables to be strings.

Copy code

```
// Build connection properties
Properties properties = new Properties();

// Required connection properties
properties.put("user"    ,  "jsmith"      );
properties.put("password",  "mypassword");
properties.put("account" ,  "myaccount");

// Set some additional variables.
properties.put("$variable_1", "some example");
properties.put("$variable_2", "1"           );

// Create a new connection
String connectStr = "jdbc:snowflake://localhost:8080";

// Open a connection under the snowflake account and enable variable support
Connection con = DriverManager.getConnection(connectStr, properties);
```

## Using variables in SQL

Variables can be used in Snowflake anywhere a literal constant is allowed, except where noted in the documentation. To distinguish them
from bind values and column names, all variables must be prefixed with a `$` sign.

For example:

Copy code

```
SET (min, max)=(40, 70);

SELECT $min;

SELECT AVG(salary) FROM emp WHERE age BETWEEN $min AND $max;
```

Note

Because the `$` sign is the prefix used to identify variables in SQL statements, it is treated as a special character when used
in identifiers. Identifiers (database names, table names, column names, and so on) can’t start with special characters unless the entire
name is enclosed in double quotes. For more information, see [Object identifiers](/sql-reference/identifiers).

Variables can also contain identifier names, such as table names. To use a variable as an identifier, you must
wrap it inside `IDENTIFIER()` (for example, `IDENTIFIER($my_variable)`). Some examples are below:

Copy code

```
SET my_table_name='table1';
```

Copy code

```
CREATE TABLE IDENTIFIER($my_table_name) (i INTEGER);
INSERT INTO IDENTIFIER($my_table_name) (i) VALUES (42);
```

Copy code

```
SELECT * FROM IDENTIFIER($my_table_name);
```

```
+----+
|  I |
|----|
| 42 |
+----+
```

In the context of a FROM clause, you can wrap the variable name in `TABLE()`, as shown below:

Copy code

```
SELECT * FROM TABLE($my_table_name);
```

```
+----+
|  I |
|----|
| 42 |
+----+
```

Copy code

```
DROP TABLE IDENTIFIER($my_table_name);
```

For more information about `IDENTIFIER()`, see [Literals and variables as identifiers with IDENTIFIER() syntax](/sql-reference/identifier-literal).

### Viewing variables for the session

To see all the variables defined in the current session, use the [SHOW VARIABLES](/sql-reference/sql/show-variables) command:

Copy code

```
SET (min, max)=(40, 70);
```

```
+----------------------------------+
| status                           |
|----------------------------------|
| Statement executed successfully. |
+----------------------------------+
```

Copy code

```
SHOW VARIABLES;
```

```
+----------------+-------------------------------+-------------------------------+------+-------+-------+---------+
|     session_id | created_on                    | updated_on                    | name | value | type  | comment |
|----------------+-------------------------------+-------------------------------+------+-------+-------+---------|
| 10363773891062 | 2024-06-28 10:09:57.990 -0700 | 2024-06-28 10:09:58.032 -0700 | MAX  | 70    | fixed |         |
| 10363773891062 | 2024-06-28 10:09:57.990 -0700 | 2024-06-28 10:09:58.021 -0700 | MIN  | 40    | fixed |         |
+----------------+-------------------------------+-------------------------------+------+-------+-------+---------+
```

### Session variable functions

The following convenience functions are provided for manipulating session variables to support compatibility with other database systems
and to issue SQL through tools that do not support the `$` syntax for accessing variables. All of these functions accept and
return session variable values as strings:

> - SYS\_CONTEXT and SET\_SYS\_CONTEXT
> - SESSION\_CONTEXT and SET\_SESSION\_CONTEXT
> - [GETVARIABLE](/sql-reference/functions/getvariable) and SETVARIABLE

Here are examples of using GETVARIABLE. First, define a variable using SET:

Copy code

```
SET var_artist_name = 'Jackson Browne';
```

```
+----------------------------------+
| status                           |
+----------------------------------+
| Statement executed successfully. |
+----------------------------------+
```

Return the variable value:

Copy code

```
SELECT GETVARIABLE('var_artist_name');
```

In this example, the output is NULL because Snowflake stores variables with all uppercase letters.

Update the casing:

Copy code

```
SELECT GETVARIABLE('VAR_ARTIST_NAME');
```

```
+--------------------------------+
| GETVARIABLE('VAR_ARTIST_NAME') |
+--------------------------------+
| Jackson Browne                 |
+--------------------------------+
```

You can use the variable name in a WHERE clause, for example:

Copy code

```
SELECT album_title
  FROM albums
  WHERE artist = $var_artist_name;
```

## Removing variables

SQL variables are private to a session. When a Snowflake session is closed, all variables created during the session are dropped. This
means that no one can access user-defined variables that have been set in another session, and when the session is closed, these variables
expire.

In addition, variables can be explicitly dropped using the [UNSET](/sql-reference/sql/unset) command.

For example:

Copy code

```
UNSET my_variable;
```
