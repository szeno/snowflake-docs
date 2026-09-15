# DESCRIBE SEARCH OPTIMIZATION

Describes the [search optimization configuration](/user-guide/search-optimization/enabling#label-search-optimization-service-add-to-table) for a specified table and
its columns.

DESCRIBE can be abbreviated to DESC.

See also:
:   [Search optimization service](/user-guide/search-optimization-service)

## Syntax

Copy code

```
DESC[RIBE] SEARCH OPTIMIZATION ON <table_name>;
```

## Parameters

`table_name`
:   Specifies the identifier for the table to describe. If the identifier contains spaces or special characters, the entire string
    must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Output

The command prints a table containing information on each search method and target in the search optimization configuration. The
table contains the following columns:

| Column Name | Description |
| --- | --- |
| `expression_id` | Unique identifier for a search method and target. |
| `method` | Search method for optimizing queries for a particular type of predicate:   - EQUALITY (for equality and IN predicates). - SUBSTRING (for predicates that match substrings – e.g. LIKE, ILIKE, etc.). - GEO (for predicates that use GEOGRAPHY types). |
| `target` | Column or VARIANT field that the method applies to. |
| `target_data_type` | Data type of the column or VARIANT field. |
| `active` | Specifies whether or not the expression has finished the initial build of the search access paths for the expression. |

Expand

Show lessSee more

## Usage notes

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

See [Displaying the search optimization configuration for a table](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-displaying).
