Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$WAIT

Waits for the specified amount of time before proceeding.

## Syntax

Copy code

```
SYSTEM$WAIT( amount [ , time_unit ] )
```

## Arguments

**Required:**

`amount`
:   Number specifying the amount of time to wait as determined by `time_unit`.

**Optional:**

`time_unit`
:   Time unit for `amount`. Accepted values are DAYS, HOURS, MINUTES, SECONDS, MILLISECONDS, MICROSECONDS, NANOSECONDS.
    The unit should be in single quotes (see [Examples](#examples) below).

    Default: SECONDS

## Usage notes

- Most systems do not have clocks that have nanosecond precision. As a result:

  - The actual wait time might not be exactly the same as the specified wait time.
  - The reported wait time might not be exact.
- SYSTEM$WAIT checks periodically for cancellation. If a user cancels a query while it is waiting, there might be a delay between the
  time the query is cancelled and the time the cancellation takes effect.
- If the wait period exceeds the compilation timeout, the query is not cancelled automatically. After the wait, the query resumes normally.

## Examples

> Copy code
>
> ```
> CALL SYSTEM$WAIT(10);
>
> -------------------+
>     SYSTEM$WAIT    |
> -------------------+
>  waited 10 seconds |
> -------------------+
> ```
>
> Copy code
>
> ```
> CALL SYSTEM$WAIT(2, 'MINUTES');
>
> -------------------+
>     SYSTEM$WAIT    |
> -------------------+
>  waited 2 minutes  |
> -------------------+
> ```
