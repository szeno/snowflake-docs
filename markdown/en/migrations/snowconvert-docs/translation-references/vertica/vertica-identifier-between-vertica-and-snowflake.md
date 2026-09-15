# Vertica - Identifier differences between Vertica and Snowflake

## Quoted identifiers

In Vertica, quoted identifiers stick to the [case sensitivity rules](https://docs.vertica.com/25.1.x/en/sql-reference/language-elements/identifiers/#case-sensitivity), which means that, for example, column names are still case insensitive even when quoted. Thus, identifiers `"ABC"`, `"ABc"`, and `"aBc"` are synonymous, as are `ABC`, `ABc`, and `aBc` :

### Vertica

Copy code

```
CREATE TABLE test.quotedIdentTable
(
  "col#1" INTEGER
);

SELECT "col#1" FROM test.quotedIdentTable;

SELECT "COL#1" FROM test.quotedIdentTable;
```

In Snowflake, case sensitivity of quoted identifiers depends on the session parameter [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case), by default quoted identifiers comparison is case sensitive, this means that the result code from migrating the above example:

### Snowflake

Copy code

```
CREATE TABLE test.quotedIdentTable
(
  "col#1" INTEGER
);

SELECT
  "col#1"
FROM
  test.quotedIdentTable;

SELECT
  "COL#1"
FROM
  test.quotedIdentTable;
```

Will fail when executing the second select unless the session parameter is set to TRUE.

## How quoted identifiers are migrated

Quoted identifiers are analyzed to determine if they contain non-alphanumeric characters or are reserved words in Snowflake, if they do they will be left as they are, alphanumeric identifiers will be left unquoted:

### Vertica

Copy code

```
CREATE TABLE test.identsTable1
(
  "col#1" INTEGER,
  "col2" INTEGER
);

-- Group is a reserved word
SELECT
"col#1" AS "group",
"col2" AS "hello"
FROM
test.identsTable1;
```

### Snowflake

Copy code

```
CREATE TABLE test.identsTable1
(
  "col#1" INTEGER,
  col2 INTEGER
);

-- Group is a reserved word
SELECT
  "col#1" AS "group",
  col2 AS hello
FROM
  test.identsTable1;
```
