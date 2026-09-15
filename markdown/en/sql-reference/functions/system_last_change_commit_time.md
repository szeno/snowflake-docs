Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$LAST\_CHANGE\_COMMIT\_TIME

Returns a token that can be used to detect whether a database table or view changed between two calls to the function.
If the token returned by a call is different from the token returned by a separate call, then the table or view
changed between the two calls, typically due to a DML operation (e.g. an INSERT).

If the specified database object is a view, then at least one of the database objects referenced by the view changed.

## Syntax

Copy code

```
SYSTEM$LAST_CHANGE_COMMIT_TIME( '<object_name>'  )
```

## Arguments

`object_name`
:   Specifies the table or view.

## Returns

The data type of the returned value is NUMBER with a scale of 0.

## Usage notes

- The value can be used in applications such as BI tools to determine whether the underlying table data has changed.
  This can be useful for applications that display dashboards and need to figure out whether the dashboard needs to be
  updated based on new data in the table.
- For each DML operation performed on the specified table or underlying tables in the specified view, the returned
  value increases.
- The value returned by the function is typically an approximation of the time that the database object was
  last changed, expressed as the UTC timestamp in nanoseconds since the beginning of the epoch (i.e. since midnight
  January 1, 1970). However, the values are only approximations, in part because the precision and skew of the
  results can vary.

  Note

  Snowflake recommends using this value only as a change indicator and strongly discourages users from treating this
  value as a timestamp.

## Examples

Copy code

```
CALL SYSTEM$LAST_CHANGE_COMMIT_TIME('mytable');

+--------------------------------+
| SYSTEM$LAST_CHANGE_COMMIT_TIME |
|--------------------------------|
|            1661920053987000000 |
+--------------------------------+
```

Copy code

```
SELECT SYSTEM$LAST_CHANGE_COMMIT_TIME('mytable');

+--------------------------------+
| SYSTEM$LAST_CHANGE_COMMIT_TIME |
|--------------------------------|
|            1661920118648000000 |
+--------------------------------+

INSERT INTO mytable VALUES (2,100), (3,300);

SELECT SYSTEM$LAST_CHANGE_COMMIT_TIME('mytable');

+--------------------------------+
| SYSTEM$LAST_CHANGE_COMMIT_TIME |
|--------------------------------|
|            1661920131893000000 |
+--------------------------------+
```
