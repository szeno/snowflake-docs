# Identifier requirements

[Unquoted object identifiers](#label-unquoted-identifier):

- Start with a letter (A-Z, a-z) or an underscore (“\_”).
- Contain only letters, underscores, decimal digits (0-9), and dollar signs (“$”).
- Are stored and resolved as uppercase characters (e.g. `id` is stored and resolved as `ID`).

If you put [double quotes around an identifier](#label-delimited-identifier) (e.g.
“My identifier with blanks and punctuation.”), the following rules apply:

- The case of the identifier is preserved when storing and resolving the identifier (e.g. `"id"` is stored and resolved as
  `id`).
- The identifier can contain and start with ASCII, extended ASCII, and non-ASCII characters.

  To use the double quote character inside a quoted identifier, use two quotes. For example:

  Copy code

  ```
  CREATE TABLE "quote""andunquote""" ...
  ```

  creates a table named:

  Copy code

  ```
  quote"andunquote"
  ```

  where the quotation marks are part of the name.

Note

- Regardless of whether an identifier is unquoted or double-quoted, the maximum number of characters allowed is 255 (including blank spaces).
- Identifiers can also be specified using string literals, session variables or bind variables. For details, see [SQL variables](/sql-reference/session-variables).

## Unquoted identifiers

If an identifier is not enclosed in double quotes, it must begin with a letter or underscore (`_`) and cannot contain extended characters or blank
spaces.

The following are all examples of valid identifiers; however, the case of the characters in these identifiers would not be preserved:

Copy code

```
myidentifier
MyIdentifier1
My$identifier
_my_identifier
```

Unquoted identifiers are stored and [resolved](#label-identifier-casing) in uppercase. Therefore, an unquoted identifier is equivalent to a capitalized double-quoted
identifier with the same name. For example, the following two statements attempt to create the same table:

Copy code

```
CREATE TABLE mytable(c1 INT, c2 INT);
```

```
+-------------------------------------+
| status                              |
|-------------------------------------|
| Table MYTABLE successfully created. |
+-------------------------------------+
```

Copy code

```
CREATE TABLE "MYTABLE"(c1 INT, c2 INT);
```

```
002002 (42710): SQL compilation error:
Object 'MYTABLE' already exists.
```

## Double-quoted identifiers

Delimited identifiers (i.e. identifiers enclosed in double quotes) are case-sensitive and can start with and contain any valid characters,
including:

- Numbers
- Special characters (`.`, `'`, `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, etc.)
- Extended ASCII and non-ASCII characters
- Blank spaces

For example:

Copy code

```
"MyIdentifier"
"my.identifier"
"my identifier"
"My 'Identifier'"
"3rd_identifier"
"$Identifier"
"идентификатор"
```

Important

If an object is created using a double-quoted identifier, when referenced in a query or any other SQL statement, the identifier must be specified
exactly as created, including the double quotes. Failure to include the quotes might result in an `Object does not exist` error (or
similar type of error).

Also, note that the entire identifier must be enclosed in quotes when referenced in a query/SQL statement. This is particularly important if periods
(`.`) are used in identifiers because periods are also used in fully-qualified object names to separate each object.

For example:

Copy code

```
"My.DB"."My.Schema"."Table.1"
```

### Exceptions

- Double-quoted identifiers are not supported for the
  [names of user-defined functions (UDFs) and procedures](/developer-guide/udf-stored-procedure-naming-conventions) in which the
  handler language is Java, JavaScript, Snowflake Scripting, or SQL.
- You can use only ASCII characters for the names of user-defined functions (UDFs) and procedures in which the handler language is Java.

## Identifier resolution

By default, Snowflake applies the following rules for storing identifiers (at creation/definition time) and resolving them (in queries and other SQL
statements):

- When an identifier is unquoted, it is stored and resolved in uppercase.
- When an identifier is double-quoted, it is stored and resolved exactly as entered, including case.

For example, the following four names are equivalent and all resolve to `TABLENAME`:

Copy code

```
TABLENAME
tablename
tableName
TableName
```

In contrast, the following four names are considered to be different, unique values:

Copy code

```
"TABLENAME"
"tablename"
"tableName"
"TableName"
```

If these identifiers were used to create objects of the same type (e.g. tables), they would result in the creation of four distinct objects.

## Migrating from databases that treat double-quoted identifiers as case-insensitive

In the ANSI/ISO standard for SQL, identifiers in double quotes (delimited identifiers) are treated as case-sensitive. However,
some companies provide databases that treat double-quoted identifiers as case-insensitive.

If you are migrating your data and applications from one of these databases to Snowflake, those applications might use double
quotes around identifiers that are intended to be case-insensitive. This can prevent Snowflake from resolving the identifiers
correctly. For example, an application might use double quotes around an identifier in lowercase, and the Snowflake database
has the identifier in uppercase.

To work around this limitation, Snowflake provides the [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](/sql-reference/parameters#label-quoted-identifiers-ignore-case) session parameter, which
causes Snowflake to treat lowercase letters in double-quoted identifiers as uppercase when creating and finding objects.

See the next sections for details:

- [Controlling case using the QUOTED\_IDENTIFIERS\_IGNORE\_CASE parameter](#label-identifier-casing-parameter-howto)
- [Impact of changing the parameter](#label-changing-quoted-identifiers-ignore-case)

Note

Changing the value of the parameter can affect your ability to find existing objects. See
[Impact of changing the parameter](#label-changing-quoted-identifiers-ignore-case) for details.

### Controlling case using the QUOTED\_IDENTIFIERS\_IGNORE\_CASE parameter

To configure Snowflake to treat alphabetic characters in double-quoted identifiers as uppercase for the session, set the
parameter to TRUE for the session. With this setting, all alphabetical characters in identifiers are stored and resolved as
uppercase characters.

In other words, the following eight names are equivalent and all resolve to `TABLENAME`:

Copy code

```
TABLENAME
tablename
tableName
TableName
"TABLENAME"
"tablename"
"tableName"
"TableName"
```

Note that the parameter has no effect on any of the limitations for unquoted identifiers with regards to numbers, extended
characters, and blank spaces.

### Impact of changing the parameter

Changing the [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](/sql-reference/parameters#label-quoted-identifiers-ignore-case) session parameter only affects new objects and queries:

- With the default setting of FALSE, if an object is created using a double-quoted identifier with mixed case, Snowflake stores
  the identifier in mixed case.
- If the parameter is later changed to TRUE, Snowflake will not be able to resolve that double-quoted mixed case identifier and
  will not be able retrieve that object.

Tip

Due to the impact that changing the parameter can have on resolving identifiers, we highly recommend choosing the
identifier resolution method early in your implementation of Snowflake. Then, have your account administrator set the parameter
at the account level to enforce this resolution method by default.

Although you can override this parameter at the session level, we don’t encourage changing the parameter from the default,
unless you have an explicit need to do so.

The following examples illustrate the behavior after changing the parameter from FALSE to TRUE:

Copy code

```
-- Set the default behavior
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = false;

-- Create a table with a double-quoted identifier
CREATE TABLE "One" (i int);  -- stored as "One"

-- Create a table with an unquoted identifier
CREATE TABLE TWO(j int);     -- stored as "TWO"

-- These queries work
SELECT * FROM "One";         -- searches for "One"
SELECT * FROM two;           -- searched for "TWO"
SELECT * FROM "TWO";         -- searches for "TWO"

-- These queries do not work
SELECT * FROM One;           -- searches for "ONE"
SELECT * FROM "Two";         -- searches for "Two"

-- Change to the all-uppercase behavior
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = true;

-- Create another table with a double-quoted identifier
CREATE TABLE "Three"(k int); -- stored as "THREE"

-- These queries work
SELECT * FROM "Two";         -- searches for "TWO"
SELECT * FROM two;           -- searched for "TWO"
SELECT * FROM "TWO";         -- searches for "TWO"
SELECT * FROM "Three";       -- searches for "THREE"
SELECT * FROM three;         -- searches for "THREE"

-- This query does not work now - "One" is not retrievable
SELECT * FROM "One";         -- searches for "ONE"
```

Additionally, if the identifiers for two tables differ only by case, one identifier might resolve to a different table after changing the parameter:

Copy code

```
-- Set the default behavior
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = false;

-- Create a table with a double-quoted identifier
CREATE TABLE "Tab" (i int);  -- stored as "Tab"

-- Create a table with an unquoted identifier
CREATE TABLE TAB(j int);     -- stored as "TAB"

-- This query retrieves "Tab"
SELECT * FROM "Tab";         -- searches for "Tab"

-- Change to the all-uppercase behavior
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = true;

-- This query retrieves "TAB"
SELECT * FROM "Tab";         -- searches for "TAB"
```
