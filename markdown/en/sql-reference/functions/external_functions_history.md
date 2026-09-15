Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# EXTERNAL\_FUNCTIONS\_HISTORY

This table function retrieves the history of external functions called by Snowflake for your entire Snowflake account.

Note

This function can return results only for activity within the last 14 days.

## Syntax

Copy code

```
EXTERNAL_FUNCTIONS_HISTORY(
      [ DATE_RANGE_START => <constant_date_expression> ]
      [, DATE_RANGE_END => <constant_date_expression> ]
      [, FUNCTION_SIGNATURE => '<string>' ] )
```

## Arguments

All the arguments are optional.

`DATE_RANGE_START => constant_date_expression` , `DATE_RANGE_END => constant_date_expression`
:   The date/time range, within the last 2 weeks, for which to retrieve the history:

    - If an end date is not specified, then [CURRENT\_DATE](/sql-reference/functions/current_date) is used as the end of the range.
    - If a start date is not specified, then the range starts 10 minutes prior to the start of `DATE_RANGE_END` (i.e. the default is to show the previous 10 minutes of history). For example,
      if `DATE_RANGE_END` is [CURRENT\_DATE](/sql-reference/functions/current_date), then the default `DATE_RANGE_START` is 11:50 PM on the previous day.

    History is displayed in increments of 5 minutes, 1 hour, or 24 hours (depending on the length of the specified range).

    If the range falls outside the last 15 days, an error is returned.

`FUNCTION_SIGNATURE => string`
:   A string specifying an external function name and the data types of the arguments to the function. (The data types
    distinguish among overloaded function names.) Only information about that function is returned.

    Put the signature inside single quotes, for example:

    > Copy code
    >
    > ```
    > function_signature => 'mydb.public.myfunction(integer, varchar)'
    > ```

    Note that the argument data types, but not the argument names, are specified.

    If no signature is specified, then the output includes the total for all external functions in use within the time
    range, and the following columns in the results display NULL:

    - FUNCTION\_NAME.
    - ARGUMENTS.
    - FUNCTION\_ENDPOINT\_URL.
    - SOURCE\_CLOUD.
    - SOURCE\_REGION.
    - TARGET\_CLOUD.
    - TARGET\_REGION.

## Usage notes

- Returns results only for the ACCOUNTADMIN role or any role that has been explicitly granted the MONITOR USAGE global privilege.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use
  or the function name EXTERNAL\_FUNCTIONS\_HISTORY must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).
- The output column named ARGUMENTS includes not only the argument data types, but also the return data type.
  The input parameter named FUNCTION\_SIGNATURE should include the data types of the arguments, but not the return data
  type.
- For troubleshooting tips, see [Troubleshooting](#label-external-functions-debugging-external-functions-history).

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range for which to return history. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range for which to return history. |
| NAME | TEXT | Name of the function for which to return history. |
| ARGUMENTS | TEXT | Data types of the arguments and of the return value. The data types of the arguments distinguish between overloaded function names. |
| FUNCTION\_ENDPOINT\_URL | TEXT | HTTPS endpoint that the function calls. This is typically a proxy service. |
| SOURCE\_CLOUD | TEXT | Cloud platform from which rows were sent (e.g. `GCP`, `Azure`, or `AWS`). |
| SOURCE\_REGION | TEXT | Region from which rows were sent (e.g. `eu-west-1`). |
| TARGET\_CLOUD | TEXT | Cloud platform to which rows were sent (e.g. `GCP`, `Azure`, or `AWS`). |
| TARGET\_REGION | TEXT | Region to which rows were sent (e.g. `eu-west-1`). |
| INVOCATIONS | NUMBER | Number of times that the remote service was called during the START\_TIME and END\_TIME window. This includes retries (e.g. due to temporary network problems). |
| SENT\_ROWS | NUMBER | Number of rows sent to the external endpoint during the START\_TIME and END\_TIME window. |
| RECEIVED\_ROWS | NUMBER | Number of rows received from the external endpoint during the START\_TIME and END\_TIME window. |
| SENT\_BYTES | NUMBER | Number of bytes sent to the external endpoint during the START\_TIME and END\_TIME window. |
| RECEIVED\_BYTES | NUMBER | Number of bytes received from the external endpoint during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Examples

Retrieve the history for a 30 minute range, in 5 minute periods, for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.external_functions_history(
>     date_range_start => to_timestamp_ltz('2020-05-24 12:00:00.000'),
>     date_range_end => to_timestamp_ltz('2020-05-24 12:30:00.000')));
> ```

Retrieve the history for the last 12 hours, in 1 hour periods, for a single external function in your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.external_functions_history(
>     date_range_start => dateadd('hour', -12, current_timestamp()),
>     function_signature => 'mydb.public.myfunction(integer, varchar)'));
> ```

Retrieve the history for the last 14 days, in 1 day periods, for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.external_functions_history(
>     date_range_start => dateadd('day', -14, current_date()),
>     date_range_end => current_date()));
> ```

Retrieve the history for the last 14 days, in 1 day periods, for a specified function in your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.external_functions_history(
>     date_range_start => dateadd('day', -14, current_date()),
>     date_range_end => current_date(),
>     function_signature => 'mydb.public.myfunction(integer, varchar)'));
> ```

## Troubleshooting

### Symptom: EXTERNAL\_FUNCTIONS\_HISTORY returns “…invalid identifier…”

Possible Cause:
:   You might not have put the function signature in single quotes. For example, the following
    is wrong because it does not include the quotes:

    Copy code

    ```
    select *
      from table(information_schema.external_functions_history(
        function_signature => mydb.public.myfunction(integer, varchar)));
    ```

Possible Solution:
:   Correct this by adding quotation marks around the function signature:

    Copy code

    ```
    select *
      from table(information_schema.external_functions_history(
        function_signature => 'mydb.public.myfunction(integer, varchar)'));
    ```

### Symptom: EXTERNAL\_FUNCTIONS\_HISTORY returns only one row of output, and many of the columns are NULL

Possible Cause:
:   You probably did not include a function signature. If you do not specify a function signature, then
    EXTERNAL\_FUNCTION\_HISTORY() returns the aggregate values for columns such as INVOCATIONS, SENT ROWS, etc., and
    returns NULL for columns such as the function name, the argument lists, etc.

Possible Solution:
:   If you intended to get information for one function, then include a function signature.

    If you intended to get information for all functions, then the NULL values for some columns are correct,
    and you do not need to fix the query.
