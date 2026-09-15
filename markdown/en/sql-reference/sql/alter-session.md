# ALTER SESSION

Sets parameters that change the behavior for the current session.

See also:
:   [SHOW PARAMETERS](/sql-reference/sql/show-parameters)

## Syntax

Copy code

```
ALTER SESSION SET sessionParams

ALTER SESSION UNSET <param_name> [ , <param_name> , ... ]
```

Where:

> Copy code
>
> ```
> sessionParams ::=
>   ABORT_DETACHED_QUERY = TRUE | FALSE
>   ACTIVE_PYTHON_PROFILER = 'LINE' | 'MEMORY'
>   AUTOCOMMIT = TRUE | FALSE
>   BINARY_INPUT_FORMAT = <string>
>   BINARY_OUTPUT_FORMAT = <string>
>   DATE_INPUT_FORMAT = <string>
>   DATE_OUTPUT_FORMAT = <string>
>   ERROR_ON_NONDETERMINISTIC_MERGE = TRUE | FALSE
>   ERROR_ON_NONDETERMINISTIC_UPDATE = TRUE | FALSE
>   GEOGRAPHY_OUTPUT_FORMAT = 'GeoJSON' | 'WKT' | 'WKB' | 'EWKT' | 'EWKB'
>   HYBRID_TABLE_LOCK_TIMEOUT = <num>
>   JSON_INDENT = <num>
>   LOG_LEVEL = <string>
>   LOCK_TIMEOUT = <num>
>   OPT_OUT_ERROR_LOGGING = TRUE | FALSE
>   PYTHON_PROFILER_TARGET_STAGE = <string>
>   PYTHON_PROFILER_MODULES = <string>
>   QUERY_TAG = <string>
>   ROWS_PER_RESULTSET = <num>
>   S3_STAGE_VPCE_DNS_NAME = <string>
>   SEARCH_PATH = <string>
>   SIMULATED_DATA_SHARING_CONSUMER = <string>
>   STATEMENT_TIMEOUT_IN_SECONDS = <num>
>   STRICT_JSON_OUTPUT = TRUE | FALSE
>   TIMESTAMP_DAY_IS_ALWAYS_24H = TRUE | FALSE
>   TIMESTAMP_INPUT_FORMAT = <string>
>   TIMESTAMP_LTZ_OUTPUT_FORMAT = <string>
>   TIMESTAMP_NTZ_OUTPUT_FORMAT = <string>
>   TIMESTAMP_OUTPUT_FORMAT = <string>
>   TIMESTAMP_TYPE_MAPPING = <string>
>   TIMESTAMP_TZ_OUTPUT_FORMAT = <string>
>   TIMEZONE = <string>
>   TIME_INPUT_FORMAT = <string>
>   TIME_OUTPUT_FORMAT = <string>
>   TRACE_LEVEL = <string>
>   TRANSACTION_DEFAULT_ISOLATION_LEVEL = <string>
>   TWO_DIGIT_CENTURY_START = <num>
>   UNSUPPORTED_DDL_ACTION = <string>
>   USE_CACHED_RESULT = TRUE | FALSE
>   WEEK_OF_YEAR_POLICY = <num>
>   WEEK_START = <num>
> ```

Note

For readability, the complete list of session parameters that can be set is not included here. For a complete list of all session parameters,
with their descriptions, as well as account and object parameters, see [Parameters](/sql-reference/parameters).

## Parameters

`SET ...`
:   Specifies one (or more) parameters to set for the session (separated by blank spaces, commas, or new lines).

    For descriptions of each of the parameters you can set for a session, see [Parameters](/sql-reference/parameters).

`UNSET ...`
:   Specifies one (or more) parameters to unset for the session, which resets them to the defaults.

    You can reset multiple parameters with a single ALTER statement; however, each property must be separated by a comma. When resetting
    a property, specify only the name; specifying a value for the property will return an error.

## Usage notes

- Parameters are typed. The supported types are BOOLEAN, NUMBER, and STRING.
- To see the current parameter values for the session, use [SHOW PARAMETERS](/sql-reference/sql/show-parameters).

## Examples

Set the lock timeout for statements executed in the session to 1 hour (3600 seconds):

> Copy code
>
> ```
> ALTER SESSION SET LOCK_TIMEOUT = 3600;
> ```

Set the lock timeout for statements executed in the session back to the default:

> Copy code
>
> ```
> ALTER SESSION UNSET LOCK_TIMEOUT;
> ```
