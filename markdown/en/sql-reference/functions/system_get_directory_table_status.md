Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_DIRECTORY\_TABLE\_STATUS

Returns a list of records that contain the [directory table](/user-guide/data-load-dirtables) consistency status for
stages in your account. Consistency status indicates whether a directory table on a replicated stage has information about (is consistent with) all of the replicated files on the stage.

See also:
:   [Stage, pipe, and load history replication](/user-guide/account-replication-stages-pipes-load-history) , [Directory tables](/user-guide/data-load-dirtables)

## Syntax

Copy code

```
SYSTEM$GET_DIRECTORY_TABLE_STATUS( [ '<stage_name>' ] )
```

## Arguments

**Optional:**

`'stage_name'`
:   Stage for which you want to retrieve the directory table consistency status. When you specify a stage name, the function returns a list
    with a single record for the directory table on that stage.

## Returns

Returns a list of directory table consistency records for each stage in your account. The list contains a maximum of 10,000 records.
If you specify a `'stage_name'` argument, the function returns a list with a single record for the directory table on that stage.

The records are in JSON format and contain the following name/value pairs:

Copy code

```
{
  "stage" : "STAGE1",
  "status" : "INCONSISTENT"
}
```

Where:

> `stage`
> :   The stage on which the directory table is enabled.
>
> `status`
> :   Consistency status for the directory table. `CONSISTENT` if the directory table is fully consistent with the replicated content
>     on the stage; `INCONSISTENT` otherwise. A status of `INCONSISTENT` means that Snowflake cannot verify consistency,
>     and that the directory table might be missing information about some files that exist on the stage.

## Usage notes

- To call this function, you must use a role that is granted or inherits the READ privilege on the stage(s) for which you want to
  retrieve consistency status.
- To update the consistency status from `INCONSISTENT` to `CONSISTENT`, perform a full refresh using the
  [ALTER STAGE … REFRESH](/sql-reference/sql/alter-stage) command.

## Examples

The following example retrieves a list of consistency status records for the stages in the account:

> Copy code
>
> ```
> SELECT SYSTEM$GET_DIRECTORY_TABLE_STATUS();
> ```
>
> Output:
>
> ```
> [
>   {
>     "stage" : "STAGE1",
>     "status" : "CONSISTENT"
>   },
>   {
>     "stage" : "STAGE2",
>     "status" : "INCONSISTENT"
>   }
> ]
> ```

The following example retrieves a consistency status record for a stage named `stage1`:

> Copy code
>
> ```
> SELECT SYSTEM$GET_DIRECTORY_TABLE_STATUS('stage1');
> ```
>
> Output:
>
> ```
> [
>   {
>     "stage" : "STAGE1",
>     "status" : "CONSISTENT"
>   }
> ]
> ```
